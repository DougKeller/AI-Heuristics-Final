require 'csv'

class Array
  def from_csv
    [
      self[0].to_f.round(2),
      self[1].to_f.round(2),
      self[2].to_f.round(2),
      self[3].to_i
    ].join(',')
  end
end

def custom_cmp(a, b)
  return a <=> b if a[-1] == b[-1]
  a[-1] <=> b[-1]
end

def add_item(argv)
  data = CSV.read('dnd/difficulty.csv') || []
  data = data.drop(1).map(&:from_csv).uniq

  new_row = argv.from_csv
  data.delete(new_row)
  data << new_row
  data = data.sort.sort! { |a, b| custom_cmp(a, b) }

  File.open('dnd/difficulty.csv', 'w') do |file|
    header = "#{data.length},3,Easy,Medium,Hard,Deadly\n"
    file.write(header)
    content = data.join("\n")
    file.write(content)
  end
end

def build_tree
  system('python dnd/estimate.py build')
end

add_item(ARGV) if ARGV.length > 0
build_tree
