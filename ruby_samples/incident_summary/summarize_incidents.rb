#!/usr/bin/env ruby
# frozen_string_literal: true

require "json"
require "time"

def read_incidents(path)
  File.readlines(path, chomp: true).map do |line|
    next if line.strip.empty?

    JSON.parse(line)
  rescue JSON::ParserError => e
    warn "Skipping malformed JSON line: #{e.message}"
    nil
  end.compact
end

def summarize(incidents)
  summary = {
    total: incidents.length,
    by_severity: Hash.new(0),
    by_service: Hash.new(0),
    unresolved: [],
    mean_resolution_minutes: nil
  }

  resolution_minutes = []

  incidents.each do |incident|
    severity = incident.fetch("severity", "unknown")
    service = incident.fetch("service", "unknown")
    opened_at = incident["opened_at"]
    resolved_at = incident["resolved_at"]

    summary[:by_severity][severity] += 1
    summary[:by_service][service] += 1

    if resolved_at.nil? || resolved_at.strip.empty?
      summary[:unresolved] << incident.fetch("id", "unknown-id")
      next
    end

    begin
      opened_time = Time.parse(opened_at)
      resolved_time = Time.parse(resolved_at)
      resolution_minutes << ((resolved_time - opened_time) / 60.0)
    rescue StandardError => e
      warn "Skipping resolution time for incident #{incident.fetch("id", "unknown-id")}: #{e.message}"
    end
  end

  unless resolution_minutes.empty?
    avg = resolution_minutes.sum / resolution_minutes.length
    summary[:mean_resolution_minutes] = avg.round(2)
  end

  summary
end

def print_summary(summary)
  puts "Incident Summary"
  puts "----------------"
  puts "Total incidents: #{summary[:total]}"
  puts

  puts "By severity:"
  summary[:by_severity].sort_by { |severity, _| severity }.each do |severity, count|
    puts "  - #{severity}: #{count}"
  end
  puts

  puts "By service:"
  summary[:by_service].sort_by { |service, _| service }.each do |service, count|
    puts "  - #{service}: #{count}"
  end
  puts

  mean_resolution = summary[:mean_resolution_minutes]
  if mean_resolution.nil?
    puts "Mean resolution time: n/a"
  else
    puts "Mean resolution time: #{mean_resolution} minutes"
  end

  if summary[:unresolved].empty?
    puts "Unresolved incidents: none"
  else
    puts "Unresolved incidents: #{summary[:unresolved].join(", ")}"
  end
end

if ARGV.length != 1
  warn "Usage: ruby summarize_incidents.rb <incidents.jsonl>"
  exit 1
end

input_path = ARGV[0]
unless File.exist?(input_path)
  warn "Input file not found: #{input_path}"
  exit 1
end

incidents = read_incidents(input_path)
summary = summarize(incidents)
print_summary(summary)
