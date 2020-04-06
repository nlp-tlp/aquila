''' Test to check whether Heroku:accounts is working... '''

require 'term/ansicolor'

# Colour-related things
# Use this trick to work around namespace cluttering that
# happens if you just include Term::ANSIColor:

class Color
	extend Term::ANSIColor
end


## Naive algorithm

def find(dirname, the_string)

	Dir.foreach(dirname) do |dir|
		dirpath = dirname + '/' + dir
		if File.directory?(dirpath) then
			if dir != '.' && dir != '..' then
				if dirpath.include? the_string
					puts "DIRECTORY:\t #{dirpath}"
				end
				find(dirpath, the_string)
			end
		else
			file = File.open(dirpath, "r")
  		data = file.read
  		if data.include? the_string
				puts "FILE:\t\t #{dirpath}"
			end
		end
	end
end







## Print out everything

def print_it(string, sub_string, string_len, sub_string_len, result, beginning, alg, c)
	time_taken = (Time.now - beginning)
	puts "\n#{alg} algorithm complete."
	puts "Time elapsed: #{"%.10f" % time_taken} seconds\n"
	puts "\n-------------------------------------------------------------------\n"
	if result.length == 0
		print c.red "The string \"#{sub_string}\" was not found."
	else		
		print c.green "The string \"#{sub_string}\" was found #{result.length} times:"
		puts "\n\n"
		i = 0
		while i < string_len
			if result.include? i
			  for j in 0..sub_string_len-1
			    print c.red string[i]
					i = i + 1
				end
			else
				print c.white string[i]
	  	  i = i + 1
		  end
		end
	end
	puts "\n-------------------------------------------------------------------\n"
end


## Initial strings, length etc

s = ARGV[1]	

sl = s.length
@c = Term::ANSIColor
beginning = Time.now


## Check which algorithm to use

alg = ARGV[0].downcase

case alg
	when "find", "f"
		puts "-" * 50
		print @c.green "Files/Directories containing \"#{s}\":\n\n"
		result = find('.', s)
		puts "-" * 50
	when "replace", "r"
		alg = "replace"
		result = replace(s)
		#print_it(s, ss, sl, ssl, result, beginning, alg, c)
	else
		print c.red "Error: "
		puts "\"#{ARGV[0]}\" is not a valid algorithm.\n"
		puts "Valid algorithms include:\n"
		puts "> Find (f)\n"
		puts "> Replace (r)\n"
end

