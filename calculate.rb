XP = [0, 0, 0, 0]
XP_LOOKUP = [
  [25,50,75,100],
  [50,100,150,200],
  [75,150,225,400],
  [125,250,375,500],
  [175,350,525,750],
  [250,500,750,1100],
  [350,700,1050,1600],
  [450,900,1400,2100],
  [550,1100,1600,2400],
  [600,1200,1900,2800],
  [800,1600,2400,3600],
  [1000,2000,3000,4500],
  [1100,2200,3400,5100],
  [1250,2500,3800,5700],
  [1400,2800,4300,6400],
  [1600,3200,4800,7200],
  [2000,3900,5900,8800],
  [2100,4200,6300,9500],
  [2400,4900,7300,10900],
  [2800,5700,8500,12700]
]

GROUP_CATS = %w(none single pair group gang mob horde)
MULTIPLIER_LOOKUPS = [0.5, 1, 1.5, 2, 2.5, 3, 4, 5];
CR_LOOKUP = [
    "0","1/8","1/4","1/2","1","2","3","4","5",
    "6","7","8","9","10","11","12","13","14","15",
    "16","17","18","19","20","21","22","23","24","25",
    "26","27","28","29","30"
]
CR_XP_LOOKUP = [
  25,
  50,
  100,
  200,
  450,
  700,
  1100,
  1800,
  2300,
  2900,
  3900,
  5000,
  5900,
  7200,
  8400,
  10000,
  11500,
  13000,
  15000,
  18000,
  20000,
  22000,
  25000,
  33000,
  41000,
  50000,
  62000,
  75000,
  90000,
  105000,
  120000,
  135000,
  155000
]

def get_cr(xp)
  cr = 0
  CR_XP_LOOKUP.each do |val|
    cr += 1 if val <= xp
  end

  CR_LOOKUP[cr]
end

def comparison(xp)
  return 0 if xp < XP[1]
  return 1 if xp < XP[2]
  return 2 if xp < XP[3]
  3
end

def xp_from_cr(cr)
  return 0 if cr == 0
  return CR_XP_LOOKUP[0] if cr <= 0.125
  return CR_XP_LOOKUP[1] if cr <= 0.25
  return CR_XP_LOOKUP[2] if cr <= 0.5
  CR_XP_LOOKUP[cr + 2]
end

def calculate(players, monsters)
  (0..3).each { |c| XP[c] = 0 }

  players.each do |player|
    XP[0] += XP_LOOKUP[player-1][0]
    XP[1] += XP_LOOKUP[player-1][1]
    XP[2] += XP_LOOKUP[player-1][2]
    XP[3] += XP_LOOKUP[player-1][3]
  end

  total_xp = 0

  monsters.each do |monster|
    total_xp += xp_from_cr(monster)
  end

  monster_total = monsters.length
  player_total = players.length

  multiplier = 0
  multiplier += 1 if monster_total > 0
  multiplier += 1 if monster_total > 1
  multiplier += 1 if monster_total > 2
  multiplier += 1 if monster_total > 6
  multiplier += 1 if monster_total > 10
  multiplier += 1 if monster_total > 14

  group_cat = GROUP_CATS[multiplier]

  if player_total < 3
    multiplier += 1
  elsif player_total >= 6
    multiplier -= 1
  end

  adjusted_xp = total_xp * MULTIPLIER_LOOKUPS[multiplier]
  difficulty = comparison(adjusted_xp)
end

require_relative 'dnd/add_case.rb'

(2..19).each do |level|
  players = Array.new(4) { level + rand(0..2) - 1 }
  monsters = Array.new(1, level)

  pavg = players.inject(:+) / players.length.to_f
  mavg = monsters.inject(:+) / monsters.length.to_f
  pstd = players.map { |v| (pavg - v) ** 2 }.inject(:+) / players.length
  mstd = monsters.map { |v| (mavg - v) ** 2 }.inject(:+) / monsters.length
  result = calculate(players,monsters)
  add_item([players.count, pavg, pstd, monsters.count, mavg, mstd, result])
end
