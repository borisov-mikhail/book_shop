import jwt
from fastapi import Response, status, Request
from src.configurations.settings import settings


def protect_by_token(f):
    async def protector(request: Request, *args, **kwargs):
        try:
            body = await request.json()
            token = body.get("token", None)
            if not token:
                return Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                content="No token provided")
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            e_mail: str = payload.get("some")
            if e_mail is None:
                return Response(status_code=status.HTTP_401_UNAUTHORIZED, content="Could not validate e_mail")
        except jwt.PyJWTError:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED, content="Could not validate e_mail")

        return await f(*args, **kwargs)

    import inspect
    protector.__signature__ = inspect.Signature(
        parameters=[
            *inspect.signature(f).parameters.values(),
            
            *filter(
                lambda p: p.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD),
                inspect.signature(protector).parameters.values()
            )
        ],
        return_annotation=inspect.signature(f).return_annotation,
    )

    return protector