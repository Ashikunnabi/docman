from functools import reduce
import operator
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, QuerySet
from django.db.models.fields.related import ForeignKey

from apps.common.exceptions import ObjectAlreadyExistsException


class BaseModelService:
    """
    Base service class for specific model
    model should be the main model of the service class
    The goal of the service is to update multiple models (but for the same APP!)
    """

    model = None

    def __init__(self, user, *args, **kwargs):
        if not user:
            raise ValueError(
                "User is required for service class: ", self.__class__.__name__
            )
        self.user = user

    def get_app_label(self):
        """
        give back the app_name, based on the model
        :return:
        """
        if self.model:
            return self.model._meta.app_label
        return None

    def user_has_permission(self, user, permission_codename):
        """
        check if the user has permission. Based on the app_label of the self.model
        :param user:
        :param permission_code:
        :return:
        """
        return user.has_perm(self.get_app_label() + "." + permission_codename)

    def get_model_field_names(self, model):
        """
        Get the name of the model fields.
        :return: set of model fields name if model is present otherwise empty set.
        """

        model_field_names_set = set()

        if model:
            for field in model._meta.get_fields():
                if isinstance(field, ForeignKey):
                    db_field_name = field.name + "_id"
                    keys = [field.name, db_field_name]
                else:
                    keys = [field.name]
                model_field_names_set.update(keys)

        return model_field_names_set

    def create_model_instance(self, model_class, **field_values):
        """
        Create model instance from given fields.

        It takes field values, checks whether the fields are valid model fields and finally create model instance from
          the fields those belongs to the given model class.

        :param model_class: Model class
        :param field_values: Values to be saved
        :return: Created model instance
        """
        filtered_fields = self.map_model_fields_and_data(field_values, model_class())
        instance = model_class(**filtered_fields)
        instance.save()
        return instance

    def create(self, *args, **kwargs):
        """
        Create instance for the model defined in the service class.
        :param args: Positional arguments (Not used).
        :param kwargs: Field values to be saved.
        :return: Created model instance.
        """
        assert self.model is not None, (
            "'%s' should either include a `model` attribute, "
            "or override the `create()` method." % self.__class__.__name__
        )
        return self.create_model_instance(self.model, **kwargs)

    def bulk_create(self, model_object_list: list) -> QuerySet:
        """
        Create bulk instance for the model defined in the service class.
        :param args: Positional arguments (Not used).
        :param kwargs: Field values to be saved.
        :return: Created model instance.
        """
        assert self.model is not None, (
            "'%s' should either include a `model` attribute, "
            "or override the `bulk_create()` method." % self.__class__.__name__
        )
        model_field_names_set = self.get_model_field_names(self.model)
        obj_list = []
        for model_obj in model_object_list:
            filtered_fields = self.map_model_fields_and_data(model_obj, self.model())
            obj_list.append(self.model(**filtered_fields))
        bulk_instance = self.model.objects.none()
        if obj_list:
            bulk_instance = self.model.objects.bulk_create(obj_list)
        return bulk_instance

    def update_model_instance(self, instance, **field_values):
        """
        Update model instance from given fields.

        It takes field values, checks whether the fields are valid model fields and finally update model instance from
          the fields those belongs to the given model class.

        :param instance: Model instance that needs to be updated
        :param field_values: Values to be updated
        :return: Updated model instance
        """
        model_class = instance.__class__
        model_field_names_set = self.get_model_field_names(model_class)
        filtered_fields = self.map_model_fields_and_data(field_values, model_class())

        for key, val in filtered_fields.items():
            setattr(instance, key, val)
        instance.save()
        return instance

    def _get_query_params(self, query_params, operator=None):
        """
        Parse the query params and filter against the model fields.

        :param query_params: Query parameter dictionary
        :param operator: Key used as or operator.
        For the syntax like field_name__or in query string '__or' is the operator. For and leave it as None.
        :return: Query parameters filter against the model fields.
        """

        model_field_names = self.get_model_field_names(self.model)
        if operator:
            op_query_params_temp = {
                key: val
                for key, val in query_params.items()
                if key.split("__")[0] in model_field_names and key.endswith(operator)
            }
            op_query_params = {}
            for key, val in op_query_params_temp.items():
                op_query_params.update({key.replace(operator, ""): val})
                query_params.pop(key)

            return op_query_params
        else:
            and_query_params = {}
            for key, val in query_params.items():
                if key.split("__")[0] in model_field_names:
                    if key.endswith("__in"):
                        val = val.split(",")
                    and_query_params.update({key: val})
            return and_query_params

    def _get_queryset(self, **query_params):
        """Filter queryset for model defined in service against the given query params.
        If there is no query params then all values in database will be returned as queryset

        :param query_params: Query parameters by which queryset will be filtered.
        :return: Filtered queryset.
        """

        assert self.model is not None, (
            "'%s' should either include a `model` attribute, "
            "or override the `read_id_by_pk()` method." % self.__class__.__name__
        )
        queryset = self.model.objects.all()

        and_query_params = self._get_query_params(query_params=query_params)

        if and_query_params:
            queryset = queryset.filter(**and_query_params)

        return queryset

    def read_by_pk(self, pk_value, **kwargs):
        """
        Read object by pk value

        :param pk_value: pk of the desired record
        :return: model instance
        """
        try:
            return self._get_queryset(**kwargs).get(pk=pk_value)
        except self.model.DoesNotExist:
            raise ObjectDoesNotExist

    def read_by_uuid(self, uuid_value, **kwargs):
        """
        Read object by uuid value

        :param uuid_value: uuid of the desired record
        :return: model instance
        """
        try:
            return self._get_queryset(**kwargs).get(uuid=uuid_value)
        except self.model.DoesNotExist:
            raise ObjectDoesNotExist

    def read_by_code(self, code_value, **kwargs):
        """
        Read object by code value

        :param code_value: code of the desired record
        :return: model instance
        """
        try:
            return self._get_queryset(**kwargs).get(code=code_value)
        except self.model.DoesNotExist:
            raise ObjectDoesNotExist

    def _get_order_by_fields(self, query_params):
        model_field_names = self.get_model_field_names(self.model)
        order_by_fields = [
            f_name
            for f_name in query_params.get("sort_order", "").split(",")
            if f_name != ""
        ]
        valid_order_by_fields = []
        for f_name in order_by_fields:
            temp_f_name = f_name[1:] if f_name.startswith("-") else f_name
            if temp_f_name in model_field_names:
                valid_order_by_fields.append(f_name)
        return valid_order_by_fields

    def _sort_queryset(self, queryset, query_params):
        if not query_params:
            return queryset

        order_by_fields = self._get_order_by_fields(query_params)
        if order_by_fields:
            queryset = queryset.order_by(*order_by_fields)

        return queryset

    def list(self, **query_params):
        """
        Retrieves the list of instances of a model. Results will be filtered by given query parameters. If the subclass
        is not related to a single model then you have to override this method in subclass.

        :param query_params: For `and` query use `field_name=value` format in query parameters.
                             For `or` and `not` query use `field_name__or=value` and `field_name__not=value` format
                             respectively in query parameters.
                             For `sorting` in query use `sort_order=field_name` and for reverse soring
                             use `sort_order=-field_name` format in query parameters.

        :return: queryset for list of instances
        """
        assert self.model is not None, (
            "'%s' should either include a `model` attribute, "
            "or override the `list()` method." % self.__class__.__name__
        )

        queryset = self._get_queryset()
        # query params
        or_query_params = self._get_query_params(
            query_params=query_params, operator="__or"
        )
        not_query_params = self._get_query_params(
            query_params=query_params, operator="__not"
        )
        and_query_params = self._get_query_params(query_params=query_params)

        if and_query_params:
            queryset = queryset.filter(**and_query_params)

        or_condition = None
        for key, val in or_query_params.items():
            temp_dict = {key: val}
            if not or_condition:
                or_condition = Q(**temp_dict)
            else:
                or_condition |= Q(**temp_dict)
        if or_condition:
            queryset = queryset.filter(or_condition)

        if not_query_params:
            queryset = queryset.exclude(**not_query_params)

        queryset = self._sort_queryset(queryset=queryset, query_params=query_params)

        if query_params.get("order_by", 1):
            if hasattr(self.model, "sort_order"):
                queryset = queryset.order_by("sort_order")
            elif hasattr(self.model, "created_at"):
                queryset = queryset.order_by("-created_at")

        return queryset

    def create_or_update(self, read_by="code", **field_values):
        """
        Update existing model if exists, otherwise create a new one.

        :param read_by: Unique value by which the model will be retrieved, like code, uuid, id etc.
        :param field_values: field values in dictionary format.
        :return: created or updated model instance
        """

        read_by_value = field_values.get(read_by, None)
        if read_by_value and hasattr(self, "read_by_" + read_by):
            try:
                model_instance = getattr(self, "read_by_" + read_by)(read_by_value)
            except ObjectDoesNotExist:
                model_instance = self.create_model_instance(self.model, **field_values)
            else:
                model_instance = self.update_model_instance(
                    model_instance, **field_values
                )
            return model_instance

    def get_id_by_uuid(self, uuid_value, **kwargs):
        """
        Get object ID by uuid value

        :param uuid_value: uuid of the desired record
        :return: ID of the model instance
        """
        try:
            model_instance = self.read_by_uuid(uuid_value, **kwargs)
        except ObjectDoesNotExist as ex:
            raise ex
        else:
            return model_instance.id

    def does_object_exist_by_code(self, code_value):
        """
        Check an object is exists or not
        :param code_value: code of the desired record
        :return: Boolean
        """
        return self.model.objects.filter(code=code_value).exists()

    def map_model_fields_and_data(self, defaults, model_class, *args, **kwargs):
        """
        For create update methods, inject tenant_code to the data dictionary if
        in the model, tenant_code is available.
        :param defaults:
        :param model_class:
        :param args:
        :param kwargs:
        :return:
        """

        model_field_names_set = self.get_model_field_names(model_class)
        filtered_fields = {
            key: val for key, val in defaults.items() if key in model_field_names_set
        }
        return filtered_fields

    def delete(self, instance):
        instance.delete()

    def get_object_or_none(self, *args, **kwargs):
        try:
            instance = self.model.objects.get(**kwargs)
        except (self.model.DoesNotExist, self.model.MultipleObjectsReturned):
            instance = None
        return instance

    def does_object_already_exists(self, *args, exclude_id=None, **kwargs):
        instance = None
        try:
            if exclude_id:
                instance = self.model.objects.exclude(id=exclude_id).get(**kwargs)
            else:
                instance = self.model.objects.get(**kwargs)
        except self.model.MultipleObjectsReturned as ex:
            raise ObjectAlreadyExistsException from ex
        except self.model.DoesNotExist:
            pass

        if instance:
            raise ObjectAlreadyExistsException
        return False

    def empty_queryset(self):
        return self.model.objects.none()
