from mongodb_migrations.base import BaseMigration
from pymongo import IndexModel, ASCENDING

class Migration(BaseMigration):

    IDX_FRETE_SELLERID_SKU = "idx_sellerid_sku"

    def upgrade(self):
        # Cria um índice único para seller_id e sku na coleção 'fretes'
        indexes = [
            IndexModel(
                [("seller_id", ASCENDING), ("sku", ASCENDING)],
                name=self.IDX_FRETE_SELLERID_SKU,
                unique=True # Garante que não haverá duplicados
            )
        ]
        self.db.fretes.create_indexes(indexes)

    def downgrade(self):
        self.db.fretes.drop_index(self.IDX_FRETE_SELLERID_SKU)