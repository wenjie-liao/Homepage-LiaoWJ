# frozen_string_literal: true

# Keep local URLs out of production, and support both user and project Pages.
# PAGES_BASE_URL is supplied by actions/configure-pages, including custom domains.
require "uri"
require "yaml"

repository = ENV.fetch("GITHUB_REPOSITORY", "").strip
unless repository.match?(%r{\A[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\z})
  abort "Set GITHUB_REPOSITORY to the actual OWNER/REPOSITORY before generating Pages configuration."
end

owner, repository_name = repository.split("/", 2)
pages_url = ENV.fetch("PAGES_BASE_URL", "").strip

if pages_url.empty?
  # PR checks do not call the Pages API, so they also work before Pages is enabled.
  origin = "https://#{owner.downcase}.github.io"
  baseurl = repository_name.casecmp?("#{owner}.github.io") ? "" : "/#{repository_name}"
else
  begin
    uri = URI.parse(pages_url)
  rescue URI::InvalidURIError => error
    abort "Invalid PAGES_BASE_URL: #{error.message}"
  end
  unless uri.is_a?(URI::HTTPS) && uri.host && !uri.userinfo && !uri.query && !uri.fragment
    abort "PAGES_BASE_URL must be an HTTPS URL without credentials, a query, or a fragment."
  end

  origin = "#{uri.scheme}://#{uri.host}"
  origin += ":#{uri.port}" unless uri.port == uri.default_port
  baseurl = uri.path.sub(%r{/+\z}, "")
end

configuration = { "url" => origin, "baseurl" => baseurl, "repository" => repository }
output = ENV.fetch("PAGES_CONFIG_OUTPUT", "_config.pages.yml")
File.write(output, YAML.dump(configuration), encoding: "UTF-8")
puts "Generated Pages configuration for #{origin}#{baseurl}/"
