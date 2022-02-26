require_relative 'fbref_scrape'
YEAR_END = 2022
YEAR_BEG = 2016

class ScrapeTeams < FbrefScrape
  attr_reader :url, :players, :base_url

  def initialize(attrs = {})
    @url = attrs[:url] || '/en/comps/9/10728/2020-2021-Premier-League-Stats'
    @base_url = 'https://fbref.com'
    @players = attrs[:players] || {}
  end

  def call
    load_from_csv
    # html = File.open('scraper/league.html')
    begin
      html = URI.open(base_url + url).read
      doc = Nokogiri::HTML.parse(html)
      title = doc.search('#info h1').text.strip
      puts "#{title}..."

      table = doc.search('.stats_table').first
      table.search('tbody tr').each do |row|
        link = row.search('a').first
        url = link.attributes['href'].value
        unless title.match?(/#{YEAR_END}/)
          puts "Scraping: #{link.text.strip}"
          @players = ScrapeTeamPlayers.new(url: url, players: @players).call
        end
        # sleep(rand(5..10)) # don't get block plz
      end

      # checks previous seasons
      prev_link = doc.search('.prevnext a').first
      prev_season_url = prev_link.attributes['href'].value
      unless prev_season_url.match?(/#{YEAR_BEG}/) || prev_link.text.strip.match?(/Next/)
        puts "Scraping: #{prev_season_url}"
        @players = ScrapeTeams.new(url: prev_season_url, players: @players).call
      end
    rescue => e
      puts "**** HTTP Error: #{e.inspect} *****"
      puts
    end
    # p @players
    save_to_csv
  end
end
