# -*- encoding : utf-8 -*-

#https://github.com/mongodb/mongo-ruby-driver/wiki/Tutorial
#https://github.com/PerfectMemory/freebase-api
require 'mongo'
require 'freebase-api'
include Mongo

class GetCategoryData 
	def get_category(k,v, network, db)
		addon = Hash.new()
		coll = db[network + ".test"]
		if network == "twitter"
			v = v.sub("#", "")
		end
		begin
			addon["_id"] = k
			results = FreebaseAPI::Topic.search(v, stemmed: "true", lang: "en,es,fr,de,it,pt,zh,ja,ko,ru,sv,fi,da,nl,el,ro,tr,hu,th,pl,cs,id,bg,uk,ca,eu,no,sl,sk,hr,sr,ar,hi,vi,fa,ga,iw,lv,lt,fil" )
			if results.nil? or results.empty?
				if network == "youtube"
					mymore = v.split("-")
					results = ""
					countf = mymore.size
					#puts mymore
					mymore.each do | m |
						m =  m.strip
						results = FreebaseAPI::Topic.search(m, stemmed: "true", lang: "en,es,fr,de,it,pt,zh,ja,ko,ru,sv,fi,da,nl,el,ro,tr,hu,th,pl,cs,id,bg,uk,ca,eu,no,sl,sk,hr,sr,ar,hi,vi,fa,ga,iw,lv,lt,fil" )
						if !(results.nil? or results.empty?)
							bestmatch = results.values.first
							matchid =  bestmatch.id
							resource = FreebaseAPI::Topic.get(matchid, filter:"commons" )
							mystuff =  resource.types
							addon["ctgl"] = mystuff
							cats = Array.new
							cats << mystuff[0]
							cats << mystuff[1]
							addon["category"] = cats
							#puts addon["category"]
							return addon
						else
							addon["category"] = "none"
							addon["ctgl"] = "none"
						end
					end
					mymore = v.split("|")
					#puts mymore
					mymore.each do | m |
						m =  m.strip
						results = FreebaseAPI::Topic.search(m, stemmed: "true", lang: "en,es,fr,de,it,pt,zh,ja,ko,ru,sv,fi,da,nl,el,ro,tr,hu,th,pl,cs,id,bg,uk,ca,eu,no,sl,sk,hr,sr,ar,hi,vi,fa,ga,iw,lv,lt,fil" )
						if !(results.nil? or results.empty?)
							bestmatch = results.values.first
							matchid =  bestmatch.id
							resource = FreebaseAPI::Topic.get(matchid, filter:"commons" )
							mystuff =  resource.types
							addon["ctgl"] = mystuff
							cats = Array.new
							cats << mystuff[0]
							cats << mystuff[1]
							addon["category"] = cats
							#puts addon["category"]
							return addon
						else
							addon["category"] = "none"
							addon["ctgl"] = "none"
						end
					end
					addon["category"] = "none"
					addon["ctgl"] = "none"
				end
				if network == "instagram"
					mymore = v.split(" ")
					results = ""
					countf = mymore.size
					#puts mymore
					mymore.each do | m |
						m =  m.strip
						results = FreebaseAPI::Topic.search(m, stemmed: "true", lang: "en,es,fr,de,it,pt,zh,ja,ko,ru,sv,fi,da,nl,el,ro,tr,hu,th,pl,cs,id,bg,uk,ca,eu,no,sl,sk,hr,sr,ar,hi,vi,fa,ga,iw,lv,lt,fil" )
						if !(results.nil? or results.empty?)
							bestmatch = results.values.first
							matchid =  bestmatch.id
							resource = FreebaseAPI::Topic.get(matchid, filter:"commons" )
							mystuff =  resource.types
							addon["ctgl"] = mystuff
							cats = Array.new
							cats << mystuff[0]
							cats << mystuff[1]
							addon["category"] = cats
							#puts addon["category"]
							return addon
						else
							addon["category"] = "none"
							addon["ctgl"] = "none"
						end
					end
				end
			else
				bestmatch = results.values.first
				matchid =  bestmatch.id
				resource = FreebaseAPI::Topic.get(matchid, filter:"commons" )
				mystuff =  resource.types
				addon["ctgl"] = mystuff
				cats = Array.new
				cats << mystuff[0]
				cats << mystuff[1]
				addon["category"] = cats
				#puts addon["category"]
				#note: we could find a pic if we needed to like this:
				#pic = FreebaseAPI.session.image(matchid, maxwidth: 150, maxheight: 150)
				#addon["pic"] = pic
			end
		rescue Exception => e  
  			puts e.message  
		end  
		return addon
	end

	def get_lookup_hash(network, db)
		#coll = db[network + ".test"]
		coll = db[network ]
		myh =  Hash.new()
		cool = coll.find.to_a
		if network != "instagram"
			cool.each do | c |
				myh[c["_id"]] = c["title"]
			end 
		else
			cool.each do | c |
				myh[c["_id"]] = c["caption"]
			end 
		end
		myhash
	end

	def update_categories(mylist,db,network)
		coll = db[network + ".test"]
		mylist.each do |m| 
			#puts coll.find("_id" => m["_id"]).to_a
			coll.update({"_id" => m["_id"]},  {"$set" => {"category" => m["category"]}}, :upsert => true)
			coll.update({"_id" => m["_id"]},  {"$set" => {"ctgl" => m["ctgl"]}}, :upsert => true)
			#puts coll.find("_id" => m["_id"]).to_a
		end
	end

	def mymain(db)
		db = Mongo::Connection.new("localhost", 27017).db("29")
		dbzs = ["google", "twitter", "instagram", "yahoo", "youtube"]
		##set the api key:
		FreebaseAPI.session = FreebaseAPI::Session.new(key: 'AIzaSyACRoRf7NLnEc0D5XcmTfBIjpJsDQkiGxM', env: :sandbox)

		dbzs.each do | network |
			puts "********************"
			puts "********************"
			puts network
			puts "********************"
			puts "********************"
			myhash = get_lookup_hash(network,db)
			#get a subset of a hash
			count = 0
		mylist = Array.new()
		newh =  Hash.new()
		myhash.each do |k, v|
			if count < 50
				newh[k] = v
				count = count + 1 
			end
			if count > 50
				next
			end
		end

		newh.each do |k,v| 
			puts "*******"
			puts v
			#puts "********"
			if v.nil? or v.empty? 
				next
			else
				catz = get_category(k,v, network,db)
				mylist << catz
				update_categories(mylist,db, network)
			end
		end
	end
end









