# require 'open-uri'
# require 'nokogiri'
# require 'pry-byebug'
require 'httparty'
# require_relative 'scrape_teams'

YEAR_END = 2022
YEAR_BEG = 2016

class ScrapeTeamPlayers
  attr_reader :tables, :players, :url, :base_url

  def initialize(attrs = {})
    @url = attrs[:url] || '/en/squads/b2b47a98/2020-2021/Newcastle-United-Stats'
    @base_url = 'https://fbref.com'
    @players = attrs[:players] || {}
    @tables = [
      { id: 'stats_standard_', columns: ['MP', 'Min', 'Gls', 'Ast', 'G-PK', 'xG', 'npxG', 'xA'] },
      { id: 'stats_keeper_', columns: [] },
      { id: 'stats_keeper_adv_', columns: [] },
      { id: 'stats_shooting_', columns: [] },
      { id: 'stats_passing_', columns: ['Att', 'Cmp', 'Prog'] },
      { id: 'stats_passing_types_', columns: [] },
      { id: 'stats_gca_', columns: ['GCA'] },
      { id: 'stats_defense_', columns: ['Press', 'Tkl', 'Blocks', 'Int', 'Clr'] },
      { id: 'stats_possession_', columns: ['Succ', 'Att Pen', 'Prog'] },
      { id: 'stats_playing_time_', columns: [] },
      { id: 'stats_misc_', columns: ['Won', 'Crs', 'Int', 'TklW'] }
    ]
  end

  def call
    # sleep(rand(1..3)) # hoping not to get blocked
    begin
      # html = File.open('scraper/test2.html')
      # html = URI.open(base_url + url).read
      full_url = base_url + url
      html = HTTParty.get(full_url).body
      doc = Nokogiri::HTML.parse(html)

      title = doc.search('#info h1').text.strip
      title_match = title.match(/^(?<first>\d{4})-?(?<second>\d{4}?)/)
      @year = title_match[:second].empty? ? title_match[:first] : title_match[:second]

      # skip if current year
      unless title.match?(/#{YEAR_END}/)
        tables.each do |table|
          next unless table[:columns]&.any?

          # get the right table
          table_element = doc.search('table').find do |element|
            element.attributes['id'].value.match?(/#{table[:id]}/)
          end
          next unless table_element

          headers = {}
          header = table_element.search('thead tr').last
          header.search('th').map.with_index do |tr, index|
            if table[:columns].include?(tr.text.strip)
              headers[index - 1] = tr.text.strip
            end
          end

          table_element.search('tbody tr').each do |row|
            # player = row.search('th').first.text.encode('UTF-8', 'binary', invalid: :replace, undef: :replace).strip
            player = row.search('th').first.text.strip
            next if player.match?(/\d/)

            # headers is OK
            headers.each do |index, col|
              player_row = row.search('td')[index]
              value = player_row.text.strip
              col_name = player_row.attributes["data-stat"].value

              @players[@year] = {} unless @players.key?(@year)
              @players[@year][player] = {} unless @players[@year].key?(player)
              @players[@year][player][col_name] = value
            end
          end
        end
      end
    rescue => e
      puts "**** HTTP Error: #{e.inspect} *****"
      puts
    end

    @players
  end
end

# "Test:"
# p ScrapeTeamPlayers.new.call
