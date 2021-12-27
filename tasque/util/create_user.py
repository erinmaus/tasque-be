from tasque.model.impl.database import SessionLocal
from fastapi import HTTPException
from tasque.logging import get_logger
import click
from ..controller.account import create_account

logger = get_logger(__name__)


@click.command()
@click.option(
    "--username", prompt="Your username", help="The username of the account to create"
)
@click.option(
    "--password",
    prompt="Your password",
    hide_input=True,
    help="The username of the account to create",
)
@click.option("--email", prompt="Your email", help="The email address of the account.")
@click.option("--name", prompt="Your name", help="The email address of the account.")
@click.option(
    "--organization-id", default=1, help="The organization ID the account belongs to."
)
def create_user(username, password, email, name, organization_id):
    db = SessionLocal()

    logger.info(f"Creating account '{username}'...")
    try:
        create_account(db, username, password, email, organization_id)
        logger.warning(f"Name '{name}' for account '{username}' not yet saved.")
        db.commit()
    except HTTPException as ex:
        logger.warn(f"Could not create account '{username}': {ex}", exc_info=True)
    except Exception as ex:
        logger.error(
            f"Unhandled error creating account for user '{username}': {ex}",
            exc_info=True,
        )


if __name__ == "__main__":
    create_user()
