import logging
import traceback

from django.http import Http404
from ninja import NinjaAPI
from ninja.errors import ValidationError

from api.apis.clients import router as client_router
from api.schemas import ValidationErrorSchema, ValidationExceptions, ExceptionSchema

api = NinjaAPI()

api.add_router('', client_router)


@api.exception_handler(ValidationError)
def validation_error(request, exc: ValidationError):
    validation_exceptions: list[ValidationExceptions] = []

    for error in exc.errors:
        validation_exceptions.append(ValidationExceptions(field='.'.join(map(str, error['loc'])),
                                                          rule=error['type'],
                                                          message=error['msg']))
    error_model = ValidationErrorSchema(exceptions=validation_exceptions, status=422, code="VALIDATION_EXCEPTION")
    return api.create_response(request, error_model.model_dump(), status=422)

@api.exception_handler(Http404)
def not_found_error(request, exc: Http404):
    error_model = ExceptionSchema(status=404, code="ENTITY_NOT_FOUND")
    return api.create_response(request, error_model.model_dump(), status=404)

@api.exception_handler(Exception)
def iternal_error(request, exc: Exception):
    error_model = ExceptionSchema(status=500, code="INTERNAL_SERVER_ERROR")
    print(traceback.format_exc())
    return api.create_response(request, error_model.model_dump(), status=500)