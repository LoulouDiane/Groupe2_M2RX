"""empty message

Revision ID: 9f9467c80c5e
Revises: 
Create Date: 2022-07-19 22:45:20.268186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f9467c80c5e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(length=64), nullable=True),
    sa.Column('postnom', sa.String(length=64), nullable=True),
    sa.Column('prenom', sa.String(length=64), nullable=True),
    sa.Column('date_naissance', sa.DateTime(), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('adresse', sa.String(length=128), nullable=True),
    sa.Column('nationalite', sa.String(length=64), nullable=True),
    sa.Column('telephone', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_clients_username'), 'clients', ['username'], unique=False)
    op.create_table('voitures',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('marque', sa.String(length=32), nullable=True),
    sa.Column('immatriculation', sa.String(length=32), nullable=True),
    sa.Column('categorie', sa.String(length=32), nullable=True),
    sa.Column('modele', sa.String(length=32), nullable=True),
    sa.Column('disponible', sa.Boolean(), nullable=True),
    sa.Column('kilometrage', sa.Integer(), nullable=True),
    sa.Column('type_voiture', sa.String(length=32), nullable=True),
    sa.Column('couleur', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_voitures_immatriculation'), 'voitures', ['immatriculation'], unique=True)
    op.create_table('locations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_location', sa.DateTime(), nullable=True),
    sa.Column('id_voiture', sa.Integer(), nullable=True),
    sa.Column('id_client', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_client'], ['clients.id'], ),
    sa.ForeignKeyConstraint(['id_voiture'], ['voitures.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('locations')
    op.drop_index(op.f('ix_voitures_immatriculation'), table_name='voitures')
    op.drop_table('voitures')
    op.drop_index(op.f('ix_clients_username'), table_name='clients')
    op.drop_table('clients')
    # ### end Alembic commands ###
