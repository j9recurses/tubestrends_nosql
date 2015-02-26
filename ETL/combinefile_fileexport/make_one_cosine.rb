#/usr/bin/ruby


def procdir_dir(dir)
  Dir[ File.join(dir, '**', '*') ].reject { |p| !File.directory? p }
end

def procdir_fil(dir)
  Dir[ File.join(dir, '**', '*.json') ].reject { |p| File.directory? p }
end

def combine_files(f, fileout)
	file = File.open(fileout, "a+")
	text=File.open(f).read
	text.each_line do |line|
		file.write(line) 
	end
	file.close
end

def get_file_name(d, outdir)
	names = d.split("/")
	filename =  names[-1]
	outdir+filename + ".json"
end

basedir = "/home/j9/spring/tubestrends/sleepymongoose/myenv/all_data/"
outdir = "/home/j9/spring/tubestrends/sleepymongoose/myenv/final_out/"

cooldirs =  procdir_dir(basedir)
puts "cool"
cooldirs.each do |d|
	myfiles = procdir_fil(d)
	filename = get_file_name(d, outdir)
	puts filename
	myfiles.each do |z|
		combine_files(z, filename)
	end
end