# -*- encoding : utf-8 -*-
require 'mongo'
include Mongo
require 'json'

def get_dbs
	dbs_ex =  Array.new()
	connection = Mongo::Connection.new
	connection.database_names.each do |name|	
 		dbs_ex << name
	end
	[dbs_ex, connection]
end

def get_collection_names(dbname, connection)
	if ( dbname =~ /2014/) 
		collz = Array.new()
		db = connection.db(dbname)
 		db.collections.each do |collection|
   			collz << collection.name
   		end
	end
	[collz, db]
end


dbsnames, connection = get_dbs
dbsnames.each do | dbname|
	puts dbname
	collz, db = get_collection_names(dbname, connection)
	if !collz.nil?
		collz.each do | mycollection| 
			if mycollection =~ /instagram/ or mycollection =~ /google/ or mycollection =~ /youtube/ or mycollection =~ /yahoo/
				coll = db[mycollection]
				puts mycollection
				f = File.open("outfiles/" +mycollection + ".json", 'w')
				newrs = coll.find.to_a
				newrs.each do |n |
					f.write(n)
				end
				f.close
			end
		end
	end
end
