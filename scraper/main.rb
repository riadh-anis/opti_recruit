require 'nokogiri'
require 'open-uri'
require_relative 'scrape_teams'
require_relative 'scrape_team_players'

@players = {}
# url = 'https://fbref.com/en/'
# html = URI.open(url).read
html = File.open('scraper/home.html')
doc = Nokogiri::HTML.parse(html)

doc.search('#leagues_primary div div p a')[1..-1].each do |comp|
  name = comp.text.strip
  puts "Scraping #{name}..."
  url = comp.attributes['href'].value
  @players = ScrapeTeams.new(url: url, players: @players).call
  p @players
  sleep(3)
end



# url = 'https://fbref.com/en/comps/9/10728/2020-2021-Premier-League-Stats'
#
