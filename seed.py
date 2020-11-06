"""Seed for sample data"""

from models import *
from app import app

# create all tables
db.drop_all()
db.create_all()

# Add users
ty = User(username='tyJ', password='password')
mike = User(username='mikeF', password='mikemike')
kade = User(username='kadeF', password='kadekade')

db.session.add_all([ty, mike, kade])
db.session.commit()

# create some lootbags
lb1 = Lootbag(name="Mike's campaign(personal)", password="mikes", owner_id=1)
lb2 = Lootbag(name="Mike's campaign(party)", password="mikesParty", owner_id=1)
lb3 = Lootbag(name="Campaign", password="BigC", owner_id=2)
lb4 = Lootbag(name="MINE", password="Christian", owner_id=3)

db.session.add_all([lb1, lb2, lb3, lb4])
db.session.commit()

# Create some items
item1 = Item(item_name='sword', rarity='common', text='1d6 slashing damage',
             requires_attunement='', slug='sword', type='Martial Weapon,Melee Weapon')
item2 = Item(item_name='Gloves of Spider Climb', rarity='uncommon', text='With these gloves, you can climb stuff',
             requires_attunement='requires attunement', slug='Gloves-of-Spider-Climb', type='Wondrous Item')

db.session.add_all([item1, item2])
db.session.commit()

# Add items to lootbags
lb_item = LootbagItem(lootbag_id=1, item_id=1)

db.session.add_all([lb_item])
db.session.commit()
