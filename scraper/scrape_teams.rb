class ScrapeTeams
  attr_reader :url, :players, :base_url

  def initialize(attrs = {})
    @url = attrs[:url] || '/en/comps/9/10728/2020-2021-Premier-League-Stats'
    @base_url = 'https://fbref.com'
    @players = attrs[:players]
  end

  def call
    # html = File.open('scraper/league.html')
    html = URI.open(base_url + url).read
    doc = Nokogiri::HTML.parse(html)
    table = doc.search('.stats_table').first
    table.search('tbody tr').each do |row|
      link = row.search('a').first
      url = link.attributes['href'].value
      puts "Scraping: #{link.text.strip}"
      @players = ScrapeTeamPlayers.new(url: url, players: @players).call
      sleep(rand(5..10)) # don't get block plz
    end
    @players
  end
end
