from app.db import SessionLocal, engine
from app.models import Base,Category,Artifact,Relationship,Trail,TrailArtifact,Exhibition,ExhibitionArtifact
Base.metadata.create_all(engine)
db=SessionLocal()
data=[
('Ancient worlds','ancient-worlds','Objects from early cities and empires.'),('Science & invention','science-invention','Tools that made the invisible measurable.'),('Art & design','art-design','Objects shaped by craft, belief, and visual language.'),('Trade & exploration','trade-exploration','Objects moving through networks of exchange.'),('Everyday life','everyday-life','The designed things that structure ordinary days.'),('Communication','communication','Technologies that carry words and knowledge.')]
for n,s,d in data:
 if not db.query(Category).filter_by(slug=s).first():db.add(Category(name=n,slug=s,description=d))
db.commit(); cats={c.slug:c.id for c in db.query(Category).all()}
objects=[
('Athenian Owl Tetradrachm','ancient-worlds','5th century BCE','Athens, Greece','silver','Athenian silver coin bearing Athena and her owl, struck in the fifth century BCE.','Its wide circulation made the owl a familiar sign of Athenian currency and commercial reach.'),
('Roman Denarius','ancient-worlds','Late Republic, 2nd–1st century BCE','Roman Republic','silver','A small silver coin used across the Roman world, often carrying political images and messages.','Coinage joined daily exchange with the public image of Roman authority.'),
('Lydian Electrum Coin','ancient-worlds','7th century BCE','Western Anatolia','electrum','Early stamped electrum coin from the region of Lydia.','Lydian coinage is among the earliest known uses of stamped precious metal for exchange.'),
('Egyptian Shabti Figure','ancient-worlds','New Kingdom, c. 1550–1070 BCE','Egypt','faience','A small funerary figure made to serve the deceased in the afterlife.','Shabtis reveal how material objects expressed beliefs about work and the afterlife.'),
('Cuneiform Administrative Tablet','ancient-worlds','c. 3100–2000 BCE','Mesopotamia','clay','A small clay tablet impressed with early cuneiform signs for record keeping.','Administrative tablets show writing emerging as a practical technology for managing goods.'),
('Greek Black-Figure Amphora','art-design','6th century BCE','Attica, Greece','terracotta','A painted storage vessel decorated with figures against a dark slip ground.','Vessels connected craft traditions with the storage and movement of wine and oil.'),
('Roman Glass Flask','everyday-life','1st–3rd century CE','Roman Empire','glass','A blown glass vessel made for storing oils or perfumes.','Glass vessels trace the spread of glassblowing and everyday personal care.'),
('Chinese Han Bronze Mirror','art-design','Han dynasty, 206 BCE–220 CE','China','bronze','A polished bronze mirror with a decorated reverse and central loop.','Mirrors combine skilled metalwork with personal ritual and domestic life.'),
('Astrolabe','science-invention','Medieval period','Islamic world','brass','A layered instrument used to model the sky and solve problems of time and direction.','Astrolabes carried mathematical astronomy into navigation, teaching, and prayer.'),
('Mariner’s Astrolabe','trade-exploration','16th century','Portugal','brass','A robust instrument adapted to estimate latitude from the sun or stars at sea.','Its use at sea linked astronomical knowledge with long-distance navigation.'),
('Sundial','science-invention','Ancient world','Mediterranean region','stone','A shadow-casting instrument that marks time by the sun’s apparent movement.','Sundials make local solar time visible and connect timekeeping to astronomy.'),
('Water Clock','science-invention','c. 3rd century BCE','Hellenistic world','bronze','A clepsydra measures time through the controlled flow of water.','Water clocks allowed time to be measured indoors and when sunlight was unavailable.'),
('Mechanical Clock Escapement','science-invention','Late medieval period','Europe','iron','The escapement regulates the release of stored energy in a mechanical clock.','Mechanical timekeeping changed how communities organized hours and public life.'),
('Pocket Watch','everyday-life','18th century','Europe','brass','A portable timepiece that brought personal timekeeping into daily routines.','Portable clocks made time a personal possession as well as a public measure.'),
('Telescope','science-invention','Early 17th century','Netherlands','glass; wood','An optical instrument that gathers light to make distant objects appear closer.','The telescope transformed astronomical observation and challenged inherited views of the cosmos.'),
('Compound Microscope','science-invention','17th century','Netherlands','glass; brass','An instrument using multiple lenses to magnify small structures.','Microscopes opened a scale of observation unavailable to the unaided eye.'),
('Movable-Type Printing Block','communication','11th century','China','ceramic','A reusable type piece from the long history of printing with movable characters.','Movable type demonstrates how technical choices respond to language and writing systems.'),
('Gutenberg Bible Leaf','communication','c. 1455','Mainz, Germany','paper; ink','A printed leaf from an early European book produced with movable metal type.','Printing enabled books to be reproduced in numbers beyond manuscript copying.'),
('Papyrus Scroll Fragment','communication','Ancient Egypt','Egypt','papyrus; ink','A fragment of writing surface made from the pith of the papyrus plant.','Papyrus supported record keeping and literary culture in the ancient Mediterranean.'),
('Quipu Recording Cord','communication','Inca period','Andes','cotton; camelid fiber','A system of knotted and colored cords used for recording information.','Quipu shows that complex record keeping need not rely on alphabetic writing.'),
('Morse Telegraph Key','communication','19th century','United States','brass; wood','A switch used to send electrical pulses in coded messages.','The telegraph made long-distance communication travel faster than physical transport.'),
('Early Telephone Receiver','communication','Late 19th century','United States','wood; metal','A receiver component from early telephone systems that carried voice over wires.','Telephony shifted communication from coded signals toward real-time spoken conversation.'),
('Porcelain Tea Bowl','everyday-life','Edo period','Japan','porcelain','A ceramic bowl used in tea preparation and serving.','Tea ware reflects how daily objects can embody ceremony, aesthetics, and social practice.'),
('Blue-and-White Porcelain Dish','trade-exploration','Ming dynasty','China','porcelain','A decorated export dish using cobalt blue under a clear glaze.','Chinese porcelain moved through extensive trade networks and inspired imitations abroad.'),
('Indigo Dyed Textile','trade-exploration','18th–19th century','South Asia','cotton; indigo dye','A cotton textile colored with indigo, a dye traded across regions.','Indigo textiles connect agricultural knowledge, skilled labor, and global commerce.'),
('Brass Compass','trade-exploration','16th–18th century','Europe','brass; iron','A magnetic compass used to maintain direction during travel.','The compass helped mariners orient themselves when coastlines were out of sight.'),
('Mechanical Calculator','science-invention','17th century','Europe','brass; wood','A geared calculating device designed to perform arithmetic mechanically.','Mechanical calculators made abstract arithmetic tangible through engineered motion.'),
('Camera Obscura','art-design','17th–19th century','Europe','wood; glass','A darkened chamber or box that projects an outside scene through a small aperture.','The camera obscura helped artists study perspective and belongs to the prehistory of photography.'),
('Daguerreotype Portrait','art-design','1840s','France','silver-plated copper; glass','A unique photographic image formed on a polished, sensitized metal plate.','Photography introduced a new way to preserve likeness and document public life.'),
('Bakelite Radio','everyday-life','1930s','United States','Bakelite; metal','A molded radio case made from an early synthetic plastic.','Bakelite brought industrial plastics into the home through consumer electronics.')]
for name,cat,period,origin,material,desc,sig in objects:
 slug=''.join(ch.lower() if ch.isalnum() else '-' for ch in name).strip('-').replace('--','-')
 if db.query(Artifact).filter_by(slug=slug).first():continue
 db.add(Artifact(name=name,slug=slug,short_description=desc,story=desc+' '+sig,historical_period=period,origin=origin,materials=material.split('; '),historical_significance=sig,tags=[cat],category_id=cats[cat],is_published=True))
db.commit(); arts={a.slug:a for a in db.query(Artifact).all()}
links=[('sundial','water-clock','shared-theme','Both make time legible through natural processes.'),('water-clock','mechanical-clock-escapement','related-technology','Mechanical clocks developed new ways to regulate measured intervals.'),('mechanical-clock-escapement','pocket-watch','related-technology','Portable watches miniaturized mechanical timekeeping.'),('athenian-owl-tetradrachm','roman-denarius','shared-theme','Both coins pair exchange with civic imagery.'),('lydian-electrum-coin','athenian-owl-tetradrachm','historical-relationship','Both belong to the early history of coinage in the Aegean world.'),('cuneiform-administrative-tablet','papyrus-scroll-fragment','shared-theme','Both are writing surfaces used to preserve information.'),('papyrus-scroll-fragment','gutenberg-bible-leaf','related-technology','Both carry written text, made reproducible through very different technologies.'),('telescope','compound-microscope','shared-theme','Optical instruments extend human observation at distant and tiny scales.'),('brass-compass','mariner-s-astrolabe','related-technology','Navigators used instruments to orient themselves and estimate position.'),('blue-and-white-porcelain-dish','indigo-dyed-textile','shared-theme','Both traveled through long-distance trade networks.')]
for s,t,k,e in links:
 if s in arts and t in arts and not db.query(Relationship).filter_by(source_artifact_id=arts[s].id,target_artifact_id=arts[t].id,relationship_type=k).first():db.add(Relationship(source_artifact_id=arts[s].id,target_artifact_id=arts[t].id,relationship_type=k,explanation=e,curated=True))
db.commit()
trails=[('How Humans Measured Time','how-humans-measured-time','Trace changing ways people marked and organized time.',['sundial','water-clock','mechanical-clock-escapement','pocket-watch']),('Objects That Changed Communication','objects-that-changed-communication','Follow technologies that carry records, text, and messages.',['cuneiform-administrative-tablet','papyrus-scroll-fragment','gutenberg-bible-leaf','morse-telegraph-key','early-telephone-receiver']),('Following the World’s Trade Routes','following-the-worlds-trade-routes','Explore materials and instruments that moved through exchange.',['lydian-electrum-coin','blue-and-white-porcelain-dish','indigo-dyed-textile','brass-compass'])]
for title,slug,desc,steps in trails:
 t=db.query(Trail).filter_by(slug=slug).first()
 if not t:t=Trail(title=title,slug=slug,description=desc,estimated_minutes=8);db.add(t);db.flush()
 if not t.steps:
  for pos,s in enumerate(steps,1):
   if s in arts:db.add(TrailArtifact(trail_id=t.id,artifact_id=arts[s].id,position=pos,step_explanation='Consider what this object reveals about changing technologies, practices, and the movement of knowledge.'))
for title,slug,desc,steps in [('Keeping Time','keeping-time','Instruments for reading and organizing time.',['sundial','water-clock','mechanical-clock-escapement','pocket-watch']),('Signals Across Distance','signals-across-distance','Objects that move information between people and places.',['cuneiform-administrative-tablet','gutenberg-bible-leaf','morse-telegraph-key','early-telephone-receiver'])]:
 e=db.query(Exhibition).filter_by(slug=slug).first()
 if not e:e=Exhibition(title=title,slug=slug,description=desc);db.add(e);db.flush()
 if not e.objects:
  for pos,s in enumerate(steps,1):
   if s in arts:db.add(ExhibitionArtifact(exhibition_id=e.id,artifact_id=arts[s].id,position=pos))
db.commit();db.close();print('Seeded 30 artifacts, categories, connections, trails, and exhibitions.')
