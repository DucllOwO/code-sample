"""InitDB

Revision ID: 7275def126ef
Revises: 
Create Date: 2024-05-27 21:40:43.350399

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text



# revision identifiers, used by Alembic.
revision = "7275def126ef"
down_revision = None
branch_labels = None
depends_on = None



def upgrade():
    op.create_table(
        'user',
        sa.Column('id', UUID(), primary_key=True, server_default=text('gen_random_uuid()')),
        sa.Column('public_address', sa.String(), nullable=False),
        sa.Column('created_time', sa.TIMESTAMP(timezone=True), server_default=text('now()')),
    )
    op.create_table(
        'project',
        sa.Column('id', UUID(), primary_key=True, server_default=text('gen_random_uuid()')),
        sa.Column('whitepage_id', UUID(), nullable=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.String()),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('owner', sa.String(), nullable=False),
        sa.Column('logo', sa.String(), nullable=False),
        sa.Column('banner', sa.String(), nullable=False),
        sa.Column('fee', sa.Float(), nullable=False, default=0.05),
        sa.Column('symbol', sa.String(), nullable=False),
        sa.Column('demo', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('chain_id', sa.String(), nullable=True),
        sa.Column('tx_hash', sa.String(), nullable=True),
        sa.Column('register_status', sa.String(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=text('now()')),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True)
    )

    op.create_table(
        'public_sale',
        sa.Column('id', UUID(), primary_key=True, server_default=text('gen_random_uuid()')),
        sa.Column('progress', sa.String(), nullable=False, default='0%'),
        sa.Column('currency', sa.String(3), nullable=False),
        sa.Column('eligibility', sa.String(20), nullable=False),
        sa.Column('prod_id', sa.String(), nullable=False),
        sa.Column('chain_id', sa.String(), nullable=True),
        sa.Column('tx_hash', sa.String(), nullable=True),
        sa.Column('start_time', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('end_time', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('min_contribution', sa.String(), nullable=False),
        sa.Column('max_contribution', sa.DECIMAL(), nullable=False),
        sa.Column('token_sales', sa.String(), nullable=False),
        sa.Column('price', sa.DECIMAL(), nullable=False),
        sa.Column('total_supply', sa.String(), nullable=False),
        sa.Column('project_id', UUID(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=text('now()')),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True)
    )

    op.create_table("presale",
        sa.Column('id', UUID(), primary_key=True, server_default=text('gen_random_uuid()')),
        sa.Column('progress', sa.String(), nullable=False, default='0%'),
        sa.Column('currency', sa.String(3), nullable=False),
        sa.Column('eligibility', sa.String(20), nullable=False),  
        sa.Column('prod_id', sa.String(), nullable=False),       
        sa.Column('chain_id', sa.String(), nullable=False),       
        sa.Column('start_time', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('end_time', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('per_ticket', sa.String(), nullable=False),
        sa.Column('per_ticket_value', sa.DECIMAL(), nullable=False),
        sa.Column('price', sa.DECIMAL(), nullable=False),
        sa.Column('token_presale', sa.String(), nullable=False),
        sa.Column('token_release', sa.String(), nullable=False),
        sa.Column('total_supply', sa.String(), nullable=False),
        sa.Column('softcap', sa.String(), nullable=False),
        sa.Column('hardcap', sa.String(), nullable=False),
        sa.Column('project_id', UUID(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=text('now()')),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True)
    )

    op.create_foreign_key(
        'fk_presale_project',
        'presale', 'project',
        ['project_id'], ['id']
    )
   
    op.create_foreign_key(
        'fk_public_sale_project',
        'public_sale', 'project',
        ['project_id'], ['id']
    )


    op.create_table(
        'channel',
        sa.Column('id', UUID(), primary_key=True, server_default=text('gen_random_uuid()')),
        sa.Column('project_id', UUID(), nullable=True),
        sa.Column('airdrop_id', UUID(), nullable=True),
        sa.Column('link', sa.String(), nullable=False),
        sa.Column('icon', sa.String(), nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=text('now()')),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True)
    )
    op.create_table(
        'airdrop',
        sa.Column('id', UUID(), primary_key=True, server_default=text('gen_random_uuid()')),
        sa.Column('token_address', sa.String(), nullable=False),
        sa.Column('airdrop_title', sa.String(), nullable=False),
        sa.Column('logo', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=text('now()')),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True)
    )
    op.create_foreign_key(
        'fk_channel_airdrop',
        'channel', 'airdrop',
        ['airdrop_id'], ['id']
    )
    op.create_foreign_key(
        'fk_channel_presale',
        'channel', 'project',
        ['project_id'], ['id']
    )
    op.create_table(
        'whitepage',
        sa.Column('id', UUID(), primary_key=True, server_default=text('gen_random_uuid()')),
        sa.Column('introduce', sa.String(), nullable=False),
        sa.Column('vision', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=text('now()')),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True)
    )
    op.create_foreign_key(
        'fk_project_whitepage',
        'project', 'whitepage',
        ['whitepage_id'], ['id']
    )
    op.create_table(
        'roadmap',
        sa.Column('id', UUID(), primary_key=True, server_default=text('gen_random_uuid()')),
        sa.Column('whitepage_id', UUID(), nullable=False),
        sa.Column('phase', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=text('now()')),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True)
    )
    op.create_foreign_key(
        'fk_roadmap_whitepage',
        'roadmap', 'whitepage',
        ['whitepage_id'], ['id']
    )
    op.create_table(
        'feature',
        sa.Column('id', UUID(), primary_key=True, server_default=text('gen_random_uuid()')),
        sa.Column('whitepage_id', UUID(), nullable=False),
        sa.Column('label', sa.String(), nullable=False),
        sa.Column('value', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=text('now()')),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True)
    )
    op.create_foreign_key(
        'fk_feature_whitepage',
        'feature', 'whitepage',
        ['whitepage_id'], ['id']
    )
    op.create_table(
        'tokenomic',
        sa.Column('id', UUID(), primary_key=True, server_default=text('gen_random_uuid()')),
        sa.Column('whitepage_id', UUID(), nullable=False),
        sa.Column('value', sa.String(), nullable=False),
        sa.Column('supply', sa.Float(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=text('now()')),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True)
    )
    op.create_foreign_key(
        'fk_tokenomic_whitepage',
        'tokenomic', 'whitepage',
        ['whitepage_id'], ['id']
    )
    op.create_table(
        'tokenomic_airdrop',
        sa.Column('id', UUID(), primary_key=True, server_default=text('gen_random_uuid()')),
        sa.Column('tokenomic_id', UUID(), nullable=False),
        sa.Column('label', sa.String(), nullable=False),
        sa.Column('rate', sa.FLOAT(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=text('now()')),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True)
    )
    op.create_foreign_key(
        'fk_tkairdrop_tokenomic',
        'tokenomic_airdrop', 'tokenomic',
        ['tokenomic_id'], ['id']
    )

    op.create_table(
        'analytic',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()')),
        sa.Column('presale_id', UUID(as_uuid=True), nullable=False),
        sa.Column('public_sale_id', UUID(as_uuid=True), nullable=False),
        sa.Column('total', sa.Float, nullable=False),
        sa.Column('prod_id', sa.String(), nullable=False),
        sa.Column('total_ticket', sa.Integer(), nullable=False),
        sa.Column('ethereum', sa.Float(), nullable=False),
        sa.Column('optimism', sa.Float(), nullable=False),
        sa.Column('arbitrum', sa.Float(), nullable=False),
        sa.Column('base', sa.Float(), nullable=False),
        sa.Column('scroll', sa.Float(), nullable=False),
        sa.Column('polygon', sa.Float(), nullable=False),
        sa.Column('binance', sa.Float(), nullable=False),
        sa.Column('pro_id', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=text('now()')),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True)
    )

    op.create_foreign_key(
        'fk_analytic_presale',
        'analytic', 'presale',
        ['presale_id'], ['id']
    )
    
    op.create_foreign_key(
        'fk_analytic_public_sale',
        'analytic', 'public_sale',
        ['public_sale_id'], ['id']
    )

    op.create_table(
        'donor',
        sa.Column('id', UUID(), primary_key=True, server_default=text('gen_random_uuid()')),
        sa.Column('tx_hash', sa.String(), nullable=False),
        sa.Column('chain_id', sa.String(), nullable=False),
        sa.Column('presale_id', UUID(), nullable=False),
        sa.Column('public_sale_id', UUID(), nullable=False),
        sa.Column('amount', sa.Float, nullable=False),
        sa.Column('amount_usd', sa.Float, nullable=False),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('pro_id', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=text('now()')),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True)
    )
    op.create_foreign_key(
        'fk_donor_presale',
        'donor', 'presale',
        ['presale_id'], ['id']
    )
    op.create_foreign_key(
        'fk_donor_public_sale',
        'donor', 'public_sale',
        ['public_sale_id'], ['id']
    )

    op.create_table(
        'staking',
        sa.Column('id', UUID(), primary_key=True, server_default=text('gen_random_uuid()')),
        sa.Column('token_address', sa.String(), nullable=False),
        sa.Column('period', sa.String(), nullable=False),
        sa.Column('min_staking_period', sa.Float(), nullable=False),
        sa.Column('min_staking_amount', sa.Float(), nullable=False),
        sa.Column('max_staking_amount', sa.Float(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=text('now()')),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True)
    )
    
    op.create_table(
        'stake',
        sa.Column('id', UUID(), primary_key=True, server_default=text('gen_random_uuid()')),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('balance', sa.Float(), nullable=False),
        sa.Column('staking_id', UUID(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=text('now()')),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True)
    )

    op.create_foreign_key(
        'fk_stake_staking',
        'stake', 'staking',
        ['staking_id'], ['id']
    )
    
    op.create_table(
        'lock',
        sa.Column('id', UUID(), primary_key=True, server_default=text('gen_random_uuid()')),
        sa.Column('token_address', sa.String),
        sa.Column('title', sa.String),
        sa.Column('amount', sa.String),
        sa.Column('unlock_date', sa.DateTime),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=text('now()')),
    )
    

def downgrade():
    op.drop_table('donor')
    op.drop_table('analytic')
    op.drop_table('channel')
    op.drop_table('presale')
    op.drop_table('public_sale')
    op.drop_table('project')
    op.drop_table('airdrop')
    op.drop_table('tokenomic_airdrop')
    op.drop_table('tokenomic')
    op.drop_table('roadmap')
    op.drop_table('feature')
    op.drop_table('stake')
    op.drop_table('staking')
    op.drop_table('lock')
    op.drop_table('whitepage')
