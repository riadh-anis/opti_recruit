require 'nokogiri'
require 'open-uri'
require 'csv'
# require_relative 'scrape_teams'
# require_relative 'scrape_team_players'
# require 'pry-byebug'

class FbrefScrape
  def initialize
    @players = {}
  end

  def call
    # url = 'https://fbref.com/en/'
    # html = URI.open(url).read
    html = File.open('scraper/home.html')
    doc = Nokogiri::HTML.parse(html)

    doc.search('#leagues_primary div div p a')[1..-1].each do |comp|
      comp_name = comp.text.strip
      puts "Scraping #{comp_name}..."
      url = comp.attributes['href'].value
      p url
      @players = ScrapeTeams.new(url: url, players: @players).call
      # sleep(3)
    end

    p @players
    save_to_csv
  end

  def save_to_csv
    @players.each do |year, players|
      CSV.open("raw_data/fbref/fbref_#{year}.csv", 'wb') do |csv|
        csv << ['name'] + players.first[1].keys
        players.each do |name, info|
          csv << [name] + info.values
        end
      end
    end
  end

  def load_from_csv
    [2018, 2019, 2020, 2021].each do |year|
      filepath = "raw_data/fbref/fbref_#{year}.csv"
      next unless File.exist?(filepath)

      CSV.foreach(filepath, headers: :first_row, header_converters: :symbol) do |row|
        @players[year] = {} unless @players.key?(year)
        player = row[:name].to_s

        @players[year][player] = row.to_h.except(:name)
      end
    end
    @players
  end
end


# p FbrefScrape.new.load_from_csv
