# Build the site with the official Jekyll engine. A normal Ruby installation
# uses its installed gems. The optional portable Windows runtime lives only
# under .tools; loading its build libraries directly avoids requiring the
# native EventMachine extension used by Jekyll's live-reload server.
require "rubygems"

root = File.expand_path("..", __dir__).tr("\\", "/")
portable_gems = File.join(".tools", "bundle", "ruby", Gem.ruby_api_version, "gems")
Dir.chdir(root) do
  if File.directory?(portable_gems)
    specifications = File.join(File.dirname(portable_gems), "specifications", "*.gemspec")
    Dir.glob(specifications).sort.each do |path|
      specification = Gem::Specification.load(path)
      next unless specification
      specification.require_paths.each do |library|
        $LOAD_PATH.unshift(File.expand_path(File.join(portable_gems, specification.full_name, library)))
      end
    end
  end
end

ENV["JEKYLL_NO_BUNDLER_REQUIRE"] = "true"
require "jekyll"

Dir.chdir(root) do
  configuration = Jekyll.configuration("source" => root, "destination" => File.join(root, "_site"))
  Jekyll::Site.new(configuration).process
  puts "Built with Jekyll #{Jekyll::VERSION}: #{configuration['destination']}"
end
