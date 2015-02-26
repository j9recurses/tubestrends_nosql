# -*- encoding : utf-8 -*-
require 'mongo'
include Mongo
require 'json'
require_relative "./freebaselookup.rb"

def procdir_dir(dir)
  Dir[ File.join(dir, '**', '*') ].reject { |p| !File.directory? p }
end

def procdir_fil(dir)
  Dir[ File.join(dir, '**', '*.json') ].reject { |p| File.directory? p }
end

def get_date_and_network_from_fname(fname)
	fstuff = fname.split("/")
    fsize = fstuff.size
    fstr = fstuff[fsize-1]
    fileinfo = fstr.split("_")
    network = fileinfo [0]
    oneday =  fileinfo[2]
    return [oneday, network]
end

def db_exists?(db)
	dbs_ex = Array.new()
	db.collections.database_names.each do |name|
 		dbs_ex << name
 	end
 	if dbs_ex.include? db
 		return true
 	end
 	return false
end

def collection_exists?(db, mycollection)
	collz = Array.new()
	db.collection_names.each do |collection|
		collz << collection
    end
    if collz.include? mycollection
    	return true
    end
    return false
end

def load_file_into_mongos(fname, oneday, network)
	connection = Mongo::Connection.new
	db = connection[oneday]
	alreadythere = collection_exists?(db, network)
	if alreadythere ==false
  		mycollection = db[network]
		File.open(fname, 'r') do |doc|  
 			while line = doc.gets  
    			h = JSON.parse(line)
    			mycollection.save(h)
    		end
    	end
    else 
    	puts "collection:" + network + " exists"
   	end
   	db
end


#mydir = "mytest/"
mydir = "/mnt/s3/tubes_trends_orig/combined_data_json"
cooldirs =  procdir_dir(mydir)
cooldirs.each do |d|
	myfiles = procdir_fil(d)
	myfiles.each do |fname| 
 		puts fname
   		oneday, network = get_date_and_network_from_fname(fname)
   		db = load_file_into_mongos(fname, oneday, network)
   		fb = GetCategoryData.new()
   		fb.mymain(oneday,network )
	end
end 	
