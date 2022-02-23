require 'nokogiri'
require 'open-uri'
require_relative 'scrape_team_players'


@players = {}
# prem_url = 'https://fbref.com/en/comps/9/10728/2020-2021-Premier-League-Stats'
# html = URI.open(url).read
html = File.open('scraper/league.html')
doc = Nokogiri::HTML.parse(html)

doc.search('#results107281_overall tbody tr').each do |row|
  link = row.search('a').first
  url = link.attributes['href'].value

  puts "Scraping info for: #{link.text.strip}"
  @players = ScrapeTeamPlayers.new(url: url, players: @players).call
  sleep(3)
end
