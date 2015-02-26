
# -*- encoding : utf-8 -*-
require 'mongo'
include Mongo
require 'json'
require_relative "./freebaselookup.rb"


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

def fix_youtube_view_count(mycollection, db)
	if ( mycollection =~ /youtube/) 
		coll = db[mycollection]
		cool = coll.find.to_a
		cool.each do | c|
			mynew = c["view_count"].to_s.gsub("[^0-9]", "").to_i
			coll.update({"_id" => c["_id"]}, {"$set" => {"view_count" => mynew }}, :upsert => true)
		end
	end
end

def fix_google_search_count(mycollection, db)
	if ( mycollection =~ /google/) 
		coll = db[mycollection]
		cool = coll.find.to_a
		cool.each do | c|
			mynew = c["search_count"].to_s.gsub(">", "").to_i
			coll.update({"_id" => c["_id"]}, {"$set" => {"search_count" => mynew }}, :upsert => true)
		end
	end
end

def fix_instagram_likes_count(mycollection, db)
	if ( mycollection =~ /instagram/) 
		coll = db[mycollection]
		cool = coll.find.to_a
		cool.each do | c|
			mynew = c["likes_count"].to_s.gsub("[+<>]", "").to_i
			coll.update({"_id" => c["_id"]}, {"$set" => {"likes_count" => mynew }}, :upsert => true)
		end
	end
end



def get_counts(mycollection, db)
	coll = db[mycollection]
	if ( mycollection =~ /instagram/) 
		#rs = coll.find().sort({"likes_count":1}).to_a
		rs = coll.find({}, :sort => ['likes_count','desc'], :limit => 20).to_a
	elsif ( mycollection =~ /google/) 
		#rs = coll.find().sort({"search_count":1}).to_a
		rs = coll.find({},  :sort => ['search_count','desc'], :limit => 20).to_a
	elsif ( mycollection =~ /youtube/) 
		#rs = coll.find().sort({"view_count":1}).to_a
		rs = coll.find({}, :sort => ['view_count','desc'], :limit => 20).to_a
	end
	rs
end

def get_category(mycollection, db, rs, dbname)
	coll = db[mycollection]
	fb = GetCategoryData.new()
	if ( mycollection =~ /instagram/) 
		network = "instagram"
		mylist = Array.new
		rs.each do | r| 
			k =  r["_id"]
			v =  r["caption"]
			catz = fb.get_category(k,v, network,db)
			puts catz
			fb.update_categories(dbname, catz,db, network)
		end
	end
	if ( mycollection =~ /google/) 
		network = "google"
		mylist = Array.new
		rs.each do | r| 
			k =  r["_id"]
			v =  r["title"]
			catz = fb.get_category(k,v, network,db)
			puts catz
			fb.update_categories(dbname, catz,db, network)
		end
	end
	if ( mycollection =~ /youtube/) 
		network = "youtube"
		mylist = Array.new
		rs.each do | r| 
			k =  r["_id"]
			v =  r["title"]
			catz = fb.get_category(k,v, network,db)
			puts catz
			fb.update_categories(dbname, catz,db, network)
		end
	end
	newrs = coll.find("category" => {"$exists" => true}).to_a
	return newrs
end

def write_to_db(newrs, mycollection)
	connection = Mongo::Connection.new
	db = connection.db("top_list")
	coll = db[mycollection]
	newrs.each do |doc|
		coll.insert(doc)
	end
end

				

dbsnames, connection = get_dbs
dbsnames.each do | dbname|
	puts dbname
	collz, db = get_collection_names(dbname, connection)
	if !collz.nil?
		collz.each do | mycollection| 
			if mycollection =~ /instagram/ or mycollection =~ /google/ or mycollection =~ /youtube/
				fix_youtube_view_count(mycollection,db)
				fix_google_search_count(mycollection, db)
				fix_instagram_likes_count(mycollection, db)
				rs = get_counts(mycollection, db)
				begin
					newrs = get_category(mycollection, db, rs, dbname)
					write_to_db(newrs, mycollection)
				rescue Exception => e  
  					puts e.message  
				end  
			end
		end
	end
end