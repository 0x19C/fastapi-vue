from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `models` ADD `user_id` INT NOT NULL;
        ALTER TABLE `models` ADD `parent_id` INT;
        ALTER TABLE `models` ADD CONSTRAINT `fk_models_users_a6fdb1d9` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
        ALTER TABLE `models` ADD CONSTRAINT `fk_models_models_3d25edbd` FOREIGN KEY (`parent_id`) REFERENCES `models` (`id`) ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `models` DROP FOREIGN KEY `fk_models_models_3d25edbd`;
        ALTER TABLE `models` DROP FOREIGN KEY `fk_models_users_a6fdb1d9`;
        ALTER TABLE `models` DROP COLUMN `user_id`;
        ALTER TABLE `models` DROP COLUMN `parent_id`;"""
