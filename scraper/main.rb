require 'nokogiri'
require 'open-uri'

players = {}

# squad_url = 'https://fbref.com/en/squads/b2b47a98/2020-2021/Newcastle-United-Stats'
# html = URI.open(squad_url).read
html = File.open('scraper/test.html')
doc = Nokogiri::HTML.parse(html)
tables = [
  { id: 'stats_standard_10728', columns: ['MP', 'xG'] },
  { id: 'stats_keeper_10728', columns: [] },
  { id: 'stats_keeper_adv_10728', columns: [] },
  { id: 'stats_shooting_10728', columns: [] },
  { id: 'stats_passing_10728', columns: [] },
  { id: 'stats_passing_types_10728', columns: [] },
  { id: 'stats_gca_10728', columns: [] },
  { id: 'stats_defense_10728', columns: ['Blocks'] },
  { id: 'stats_possession_10728', columns: [] },
  { id: 'stats_playing_time_10728', columns: [] },
  { id: 'stats_misc_10728', columns: [] }
]

tables.each do |table|
  next unless table[:columns]&.any?

  table_element = doc.search("##{table[:id]}")

  headers = {}
  header = table_element.search('thead tr').last
  header.search('th').map.with_index do |tr, index|
    headers[index - 1] = tr.text.strip if table[:columns].include?(tr.text.strip)
  end

  table_element.search('tbody tr').each do |row|
    player = row.search('th').first.text.strip
    headers.each do |index, col|
      player_row = row.search('td')[index]
      value = player_row.text.strip
      col_name = player_row.attributes["data-stat"].value

      players[player] = {} unless players.key?(player)
      players[player][col_name] = value
    end
  end
end

p players
