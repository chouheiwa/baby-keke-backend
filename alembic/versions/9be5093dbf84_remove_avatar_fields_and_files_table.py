"""remove_avatar_fields_and_files_table

Revision ID: 9be5093dbf84
Revises: c9e0005142cf
Create Date: 2025-11-10 15:23:49.885198

移除头像字段和文件表：
- 从 users 表删除 avatar_url 字段
- 从 babies 表删除 avatar_url 字段
- 删除 files 表
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '9be5093dbf84'
down_revision: Union[str, None] = 'c9e0005142cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """执行升级：移除头像字段和文件表"""

    # 禁用外键检查（MySQL）
    op.execute("SET FOREIGN_KEY_CHECKS=0")

    try:
        # 1. 删除 files 表（如果存在）
        op.execute("DROP TABLE IF EXISTS files")

        # 2. 从 users 表删除 avatar_url 字段
        # 使用存储过程方式兼容不同 MySQL 版本
        op.execute("""
            DROP PROCEDURE IF EXISTS drop_users_avatar_url
        """)
        op.execute("""
            CREATE PROCEDURE drop_users_avatar_url()
            BEGIN
                IF EXISTS (
                    SELECT * FROM information_schema.COLUMNS
                    WHERE TABLE_SCHEMA = DATABASE()
                    AND TABLE_NAME = 'users'
                    AND COLUMN_NAME = 'avatar_url'
                ) THEN
                    ALTER TABLE users DROP COLUMN avatar_url;
                END IF;
            END
        """)
        op.execute("CALL drop_users_avatar_url()")
        op.execute("DROP PROCEDURE drop_users_avatar_url")

        # 3. 从 babies 表删除 avatar_url 字段
        op.execute("""
            DROP PROCEDURE IF EXISTS drop_babies_avatar_url
        """)
        op.execute("""
            CREATE PROCEDURE drop_babies_avatar_url()
            BEGIN
                IF EXISTS (
                    SELECT * FROM information_schema.COLUMNS
                    WHERE TABLE_SCHEMA = DATABASE()
                    AND TABLE_NAME = 'babies'
                    AND COLUMN_NAME = 'avatar_url'
                ) THEN
                    ALTER TABLE babies DROP COLUMN avatar_url;
                END IF;
            END
        """)
        op.execute("CALL drop_babies_avatar_url()")
        op.execute("DROP PROCEDURE drop_babies_avatar_url")

    finally:
        # 重新启用外键检查
        op.execute("SET FOREIGN_KEY_CHECKS=1")


def downgrade() -> None:
    """执行降级：恢复头像字段和文件表"""

    # 禁用外键检查（MySQL）
    op.execute("SET FOREIGN_KEY_CHECKS=0")

    try:
        # 1. 恢复 users 表的 avatar_url 字段
        op.add_column('users',
            sa.Column('avatar_url', mysql.VARCHAR(length=500), nullable=True, comment='头像URL')
        )

        # 2. 恢复 babies 表的 avatar_url 字段
        op.add_column('babies',
            sa.Column('avatar_url', mysql.VARCHAR(length=500), nullable=True, comment='宝宝头像')
        )

        # 3. 重新创建 files 表
        op.create_table('files',
            sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='文件ID'),
            sa.Column('cos_key', mysql.VARCHAR(length=500), nullable=False, comment='COS对象键（文件路径）'),
            sa.Column('file_id', mysql.VARCHAR(length=100), nullable=True, comment='文件ID（微信云托管fileid）'),
            sa.Column('bucket', mysql.VARCHAR(length=100), nullable=False, comment='存储桶名称'),
            sa.Column('region', mysql.VARCHAR(length=50), nullable=False, comment='COS地域'),
            sa.Column('file_name', mysql.VARCHAR(length=255), nullable=False, comment='原始文件名'),
            sa.Column('file_size', sa.BigInteger(), nullable=False, comment='文件大小（字节）'),
            sa.Column('content_type', mysql.VARCHAR(length=100), nullable=True, comment='MIME类型'),
            sa.Column('file_url', mysql.VARCHAR(length=1000), nullable=True, comment='文件访问URL'),
            sa.Column('etag', mysql.VARCHAR(length=100), nullable=True, comment='文件ETag（用于校验）'),
            sa.Column('related_type',
                sa.Enum('BABY_AVATAR', 'GROWTH_PHOTO', 'FEEDING_PHOTO', 'DIAPER_PHOTO', 'SLEEP_PHOTO', 'OTHER'),
                nullable=False,
                comment='关联类型'
            ),
            sa.Column('related_id', sa.Integer(), nullable=True, comment='关联记录ID（如baby_id, record_id等）'),
            sa.Column('uploaded_by', sa.Integer(), nullable=False, comment='上传用户ID'),
            sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False, comment='创建时间'),
            sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False, comment='更新时间'),
            sa.PrimaryKeyConstraint('id'),
            sa.ForeignKeyConstraint(['uploaded_by'], ['users.id'], ),
            mysql_collate='utf8mb4_unicode_ci',
            mysql_default_charset='utf8mb4',
            mysql_engine='InnoDB',
            comment='文件存储表'
        )
        op.create_index('idx_cos_key', 'files', ['cos_key'], unique=True)
        op.create_index('idx_file_id', 'files', ['file_id'], unique=False)
        op.create_index('idx_uploaded_by', 'files', ['uploaded_by'], unique=False)

    finally:
        # 重新启用外键检查
        op.execute("SET FOREIGN_KEY_CHECKS=1")
