from rest_framework.renderers import JSONRenderer


class APIJSONRenderer(JSONRenderer):
    base_format = {"message": ""}
    success_format = {"success": True, "meta": {}, **base_format}
    failure_format = {"success": False}

    def set_error_response(self, data):
        errors = data.get("errors")
        message = data.get("message")

        if not errors:
            errors = data

        self.failure_format.update(message=message, error=errors)

    def get_proper_response(self, data):
        meta = {}

        if isinstance(data, dict):
            if "meta" in data.keys():
                meta = data.pop("meta")

            # an error occurs
            if "errors" in data:
                self.set_error_response(data=data)
                return self.failure_format

            # DataTable format
            if "draw" in data:
                self.success_format.update(
                    draw=data.pop("draw", 0),
                    recordsTotal=data.pop("recordsTotal", 0),
                    recordsFiltered=data.pop("recordsFiltered", 0),
                )

                data = data.pop("data", [])
            self.success_format.update(data=data, meta=meta)
            return self.success_format

        self.success_format.update(
            meta=meta, data=data, recordsTotal=len(data) if data else 0
        )
        return self.success_format

    def render(self, data, accepted_media_type=None, renderer_context=None):
        data = self.get_proper_response(data=data)

        return super().render(
            data=data,
            accepted_media_type=accepted_media_type,
            renderer_context=renderer_context,
        )
