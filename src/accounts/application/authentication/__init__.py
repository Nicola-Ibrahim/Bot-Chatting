# import inspect

# from django.contrib.auth import _clean_credentials, _get_backends
# from django.contrib.auth.signals import user_login_failed
# from django.views.decorators.debug import sensitive_variables



# @sensitive_variables("credentials")
# def authenticate(request=None, **credentials):
#     """
#     If the given credentials are valid, return a User object.
#     """
#     for backend, backend_path in _get_backends(return_tuples=True):
#         backend_signature = inspect.signature(backend.authenticate)
#         try:
#             backend_signature.bind(request, **credentials)
#         except TypeError:
#             # This backend doesn't accept these credentials as arguments. Try
#             # the next one.
#             continue

#         user = backend.authenticate(request, **credentials)

#         if user is None:
#             continue
#         # Annotate the user object with the path of the backend.
#         user.backend = backend_path
#         return user

#     # The credentials supplied are invalid to all backends, fire signal
#     user_login_failed.send(sender=__name__, credentials=_clean_credentials(credentials), request=request)
