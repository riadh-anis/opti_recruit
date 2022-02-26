# require 'open-uri'
# require 'nokogiri'
class ScrapeTeamPlayers
  attr_reader :tables, :players, :url, :base_url

  def initialize(attrs = {})
    @url = attrs[:url] || '/en/squads/b2b47a98/2020-2021/Newcastle-United-Stats'
    @base_url = 'https://fbref.com'
    @players = attrs[:players] || {}
    @tables = [
      { id: 'stats_standard_', columns: ['MP', 'xG'] },
      { id: 'stats_keeper_', columns: [] },
      { id: 'stats_keeper_adv_', columns: [] },
      { id: 'stats_shooting_', columns: [] },
      { id: 'stats_passing_', columns: [] },
      { id: 'stats_passing_types_', columns: [] },
      { id: 'stats_gca_', columns: [] },
      { id: 'stats_defense_', columns: ['Blocks'] },
      { id: 'stats_possession_', columns: [] },
      { id: 'stats_playing_time_', columns: [] },
      { id: 'stats_misc_', columns: [] }
    ]
  end

  def call
    # html = File.open('scraper/test.html')
    html = URI.open(base_url + url).read
    doc = Nokogiri::HTML.parse(html)

    tables.each do |table|
      next unless table[:columns]&.any?

      # p table_element = doc.search("##{table[:id]}:regex('[0-9]+')")
      table_element = doc.xpath("//table[starts-with(@id, #{table[:id]})]")

      headers = {}
      header = table_element.search('thead tr').last
      header.search('th').map.with_index do |tr, index|
        headers[index - 1] = tr.text.strip if table[:columns].include?(tr.text.strip)
      end

      table_element.search('tbody tr').each do |row|
        player = row.search('th').first.text.encode('UTF-8', 'binary', invalid: :replace, undef: :replace).strip
        next if player.match?(/\d/)

        headers.each do |index, col|
          player_row = row.search('td')[index]
          value = player_row.text.strip
          col_name = player_row.attributes["data-stat"].value

          @players[player] = {} unless @players.key?(player)
          @players[player][col_name] = value
        end
      end
    end
    @players
  end
end

# "Test:"
# p ScrapeTeamPlayers.new.call
