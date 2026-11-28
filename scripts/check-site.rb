# frozen_string_literal: true

require "cgi"
require "uri"
require "pathname"
require "json"

root = File.expand_path(ARGV[0] || "_site")
prefix = (ARGV[1] || "").sub(%r{/$}, "")
errors = []
pages = Dir[File.join(root, "**", "*.html")]
abort "No built pages found at #{root}" if pages.empty?
required = %w[index.html research/index.html publications/index.html software/index.html teaching/index.html about/index.html contact/index.html]
required += required.map { |file| "zh/#{file}" }
required.each { |file| errors << "Missing required page: #{file}" unless File.file?(File.join(root, file)) }
%w[papers teach teaching].each do |folder|
  private_directory = File.join(root, "assets", folder)
  errors << "Private source material found in build: #{private_directory}" if File.exist?(private_directory) || File.symlink?(private_directory)
end
references = 0
pages.each do |file|
  html = File.read(file, encoding: "UTF-8")
  rel = Pathname.new(file).relative_path_from(Pathname.new(root)).to_s
  errors << "Template sample text remains in #{rel}" if html.match?(/Albert Einstein|you@example\.com|Write your biography here|555 your office/)
  errors << "Unrendered Liquid in #{rel}" if html.match?(/\{%|\{\{/)
  # Each page has a matching locale and a switch to its exact counterpart.
  chinese = rel.start_with?("zh/")
  expected_language = chinese ? "zh-CN" : "en"
  errors << "Wrong HTML language in #{rel}" unless html.match?(/<html[^>]*lang=["']#{expected_language}["']/)
  counterpart = chinese ? rel.delete_prefix("zh/") : "zh/#{rel}"
  counterpart = counterpart.delete_suffix("index.html")
  expected_switch = prefix + "/" + counterpart
  switch = html[/<a\b[^>]*class=["']language-switch["'][^>]*>/]
  switch_href = switch && switch[/href=["']([^"']+)["']/, 1]
  errors << "Missing or incorrect language switch in #{rel}" unless switch_href == expected_switch
  errors << "Removed English university profile link remains in #{rel}" if html.include?("https://faculty.swjtu.edu.cn/liaowj/en/index.htm")
  decoded_html = URI::DEFAULT_PARSER.unescape(CGI.unescapeHTML(html))
  errors << "Private source reference in #{rel}" if decoded_html.match?(%r{(?:/|\\)assets(?:/|\\)(?:papers|teach|teaching)(?:/|\\)}i)
  html.scan(/(?:href|src)\s*=\s*["']([^"']+)["']/i).flatten.each do |raw|
    url = CGI.unescapeHTML(raw)
    next if url.match?(%r{\A(?:[a-z][a-z0-9+.-]*:|//|#)}i)
    path = URI::DEFAULT_PARSER.unescape(url.split(/[?#]/, 2).first.to_s)
    next if path.empty?
    if path.start_with?("/")
      unless prefix.empty? || path == prefix || path.start_with?(prefix + "/")
        errors << "Path misses deployment prefix in #{rel}: #{path}"
        next
      end
      path = path.delete_prefix(prefix).sub(%r{\A/+}, "")
      target = File.expand_path(path, root)
    else
      target = File.expand_path(path, File.dirname(file))
    end
    target = File.join(target, "index.html") if File.directory?(target)
    references += 1
    errors << "Broken local reference in #{rel}: #{url}" unless File.file?(target) && target.start_with?(root + File::SEPARATOR)
  end
end
# Validate publication completeness directly against the shared data source.
data_file = File.expand_path("../_data/publications.json", __dir__)
abort "Missing publication data: #{data_file}" unless File.file?(data_file)
papers = JSON.parse(File.read(data_file, encoding: "UTF-8"))
abort "Publication data must be a nonempty array" unless papers.is_a?(Array) && !papers.empty?
ids = papers.map { |paper| paper.fetch("id") }
errors << "Duplicate publication IDs in data" unless ids.uniq.length == ids.length
publication_pages = { "publications/index.html" => ids }
papers.flat_map { |paper| paper.fetch("themes") }.uniq.each do |theme|
  publication_pages["research/#{theme}/index.html"] = papers.select { |paper| paper.fetch("themes").include?(theme) }.map { |paper| paper.fetch("id") }
end
publication_pages.merge!(publication_pages.transform_keys { |path| "zh/#{path}" })
publication_pages.each do |relative, expected_ids|
  file = File.join(root, relative)
  unless File.file?(file)
    errors << "Missing publication listing: #{relative}"
    next
  end
  listed_ids = File.read(file, encoding: "UTF-8").scan(/\bid=["']paper-([^"']+)["']/).flatten
  expected_ids.each do |id|
    count = listed_ids.count(id)
    errors << "Expected publication #{id} exactly once in #{relative}, found #{count}" unless count == 1
  end
  unexpected = listed_ids - expected_ids
  errors << "Unexpected publications in #{relative}: #{unexpected.uniq.join(', ')}" unless unexpected.empty?
end
papers.each do |paper|
  figure = paper.fetch("figure", "")
  if figure.empty? || !figure.start_with?("/assets/img/")
    errors << "Missing or invalid method figure for #{paper.fetch('id')}"
    next
  end
  target = File.expand_path(figure.delete_prefix("/"), root)
  unless target.start_with?(root + File::SEPARATOR) && File.file?(target)
    errors << "Missing method figure for #{paper.fetch('id')}: #{figure}"
  end
end
# All content must be available in both languages without exposing course originals.
teaching = JSON.parse(File.read(File.expand_path("../_data/teaching.json", __dir__), encoding: "UTF-8"))
["teaching/index.html", "zh/teaching/index.html"].each do |relative|
  file = File.join(root, relative)
  next unless File.file?(file)
  html = File.read(file, encoding: "UTF-8")
  language = relative.start_with?("zh/") ? "zh" : "en"
  teaching.each do |course|
    title = language == "zh" ? course.fetch("title_zh") : course.fetch("title")
    errors << "Missing course #{course.fetch('id')} in #{relative}" unless CGI.unescapeHTML(html).include?(title)
  end
end
papers.each do |paper|
  %w[title_zh summary_zh figure_caption_zh].each do |field|
    errors << "Missing #{field} for #{paper.fetch('id')}" if paper.fetch(field, "").empty?
  end
end
abort errors.uniq.join("\n") unless errors.empty?
puts "PASS: #{pages.length} HTML pages, #{references} local references, #{papers.length} publications, required pages and privacy checks."
