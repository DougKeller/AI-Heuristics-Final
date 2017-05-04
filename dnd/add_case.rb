require 'csv'

class Array
  def from_csv
    [
      self[0].to_i,
      self[1].to_f,
      self[2].to_i,
      self[3].to_f,
      self[4].to_i
    ].join(',')
  end
end

data = CSV.read('dnd/difficulty.csv') || []
data = data.drop(1).map(&:from_csv)

new_row = ARGV.from_csv
data << new_row unless data.include? new_row
data = data.sort.sort! { |a, b| a[-1] <=> b[-1] }

File.open('dnd/difficulty.csv', 'w') do |file|
  header = "#{data.length},4,Easy,Medium,Hard,Deadly\n"
  file.write(header)
  content = data.join("\n")
  file.write(content)
end