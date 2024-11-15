"""empty message

Revision ID: 89b4aee0f80b
Revises: 
Create Date: 2024-11-04 14:43:16.519004

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '89b4aee0f80b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.String(length=120),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=mysql.VARCHAR(length=20),
               type_=sa.String(length=60),
               existing_nullable=False)
        batch_op.alter_column('join_time',
               existing_type=mysql.DATETIME(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('join_time',
               existing_type=mysql.DATETIME(),
               nullable=True)
        batch_op.alter_column('password',
               existing_type=sa.String(length=60),
               type_=mysql.VARCHAR(length=20),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.String(length=120),
               type_=mysql.VARCHAR(length=50),
               existing_nullable=False)

    # ### end Alembic commands ###
