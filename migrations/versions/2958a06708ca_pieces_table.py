"""pieces table

Revision ID: 2958a06708ca
Revises: ac41436f2c52
Create Date: 2022-11-08 20:48:14.266748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2958a06708ca'
down_revision = 'ac41436f2c52'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('piece', sa.Column('title', sa.String(length=64), nullable=True))
    op.add_column('piece', sa.Column('author', sa.String(length=64), nullable=True))
    op.add_column('piece', sa.Column('AudioDirectory', sa.String(length=256), nullable=True))
    op.add_column('piece', sa.Column('SheetDirectory', sa.String(length=256), nullable=True))
    op.add_column('piece', sa.Column('key', sa.String(length=64), nullable=True))
    op.add_column('piece', sa.Column('bpm', sa.Integer(), nullable=True))
    op.add_column('piece', sa.Column('timeSignature', sa.String(length=4), nullable=True))
    op.drop_column('piece', 'body')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('piece', sa.Column('body', sa.VARCHAR(length=140), nullable=True))
    op.drop_column('piece', 'timeSignature')
    op.drop_column('piece', 'bpm')
    op.drop_column('piece', 'key')
    op.drop_column('piece', 'SheetDirectory')
    op.drop_column('piece', 'AudioDirectory')
    op.drop_column('piece', 'author')
    op.drop_column('piece', 'title')
    # ### end Alembic commands ###
