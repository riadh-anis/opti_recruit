require 'nokogiri'
require 'open-uri'
require 'csv'
require_relative 'scrape_teams'
require_relative 'scrape_team_players'

# YEAR_END = 2022
# YEAR_BEG = 2018
@players = {}


# url = 'https://fbref.com/en/'
# html = URI.open(url).read
html = File.open('scraper/home.html')
doc = Nokogiri::HTML.parse(html)

doc.search('#leagues_primary div div p a')[1..1].each do |comp|
  comp_name = comp.text.strip
  puts "Scraping #{comp_name}..."
  url = comp.attributes['href'].value
  p url
  @players = ScrapeTeams.new(url: url, players: @players).call
  sleep(3)
end

p @players

@players.each do |year, players|
  CSV.open("raw_data/fbref/fbref_#{year}.csv", 'wb') do |csv|
    csv << ['name'] + players.first[1].keys
    players.each do |name, info|
      csv << [name] + info.values
    end
  end
end

# url = 'https://fbref.com/en/comps/9/10728/2020-2021-Premier-League-Stats'
