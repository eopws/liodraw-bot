from aiogram import Router


def setup_routers() -> Router:
    from . import usermode, adminmode, ban # unsupported_reply, message_edit, usermode

    router = Router()

    # router.include_router(unsupported_reply.router)
    # router.include_router(message_edit.router)

    router.include_router(ban.router)
    router.include_router(adminmode.router)
    router.include_router(usermode.router)

    return router
