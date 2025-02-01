from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `datasetconvertlog` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `brightness` DOUBLE NOT NULL,
    `noise` DOUBLE NOT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `origin_id` INT NOT NULL,
    `target_id` INT NOT NULL,
    CONSTRAINT `fk_datasetc_datasets_e3f303e0` FOREIGN KEY (`origin_id`) REFERENCES `datasets` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_datasetc_datasets_800e8e35` FOREIGN KEY (`target_id`) REFERENCES `datasets` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
        CREATE TABLE IF NOT EXISTS `modelconvertlog` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `dataset_convert_log_id` INT NOT NULL,
    `origin_id` INT NOT NULL,
    `target_id` INT NOT NULL,
    CONSTRAINT `fk_modelcon_datasetc_e164bf19` FOREIGN KEY (`dataset_convert_log_id`) REFERENCES `datasetconvertlog` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_modelcon_models_0886b8e5` FOREIGN KEY (`origin_id`) REFERENCES `models` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_modelcon_models_028ca8d6` FOREIGN KEY (`target_id`) REFERENCES `models` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `modelconvertlog`;
        DROP TABLE IF EXISTS `datasetconvertlog`;"""
