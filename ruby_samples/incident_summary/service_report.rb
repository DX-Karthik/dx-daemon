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

def build_service_report(incidents)
  by_service = Hash.new { |hash, key| hash[key] = { total: 0, unresolved: 0, resolution_minutes: [] } }

  incidents.each do |incident|
    service = incident.fetch("service", "unknown")
    opened_at = incident["opened_at"]
    resolved_at = incident["resolved_at"]

    by_service[service][:total] += 1

    if resolved_at.nil? || resolved_at.strip.empty?
      by_service[service][:unresolved] += 1
      next
    end

    begin
      opened_time = Time.parse(opened_at)
      resolved_time = Time.parse(resolved_at)
      by_service[service][:resolution_minutes] << ((resolved_time - opened_time) / 60.0)
    rescue StandardError => e
      warn "Skipping time parse for #{service}: #{e.message}"
    end
  end

  by_service.map do |service, data|
    avg_resolution = if data[:resolution_minutes].empty?
      nil
    else
      (data[:resolution_minutes].sum / data[:resolution_minutes].length).round(2)
    end

    unresolved_rate = ((data[:unresolved].to_f / data[:total]) * 100).round(2)

    {
      service: service,
      total_incidents: data[:total],
      unresolved_incidents: data[:unresolved],
      unresolved_rate_percent: unresolved_rate,
      average_resolution_minutes: avg_resolution
    }
  end.sort_by { |row| [-row[:unresolved_rate_percent], -row[:total_incidents], row[:service]] }
end

def print_report(rows)
  puts "Service Reliability Report"
  puts "--------------------------"
  puts "service,total,unresolved,unresolved_rate_percent,avg_resolution_minutes"
  rows.each do |row|
    avg = row[:average_resolution_minutes].nil? ? "n/a" : row[:average_resolution_minutes]
    puts [
      row[:service],
      row[:total_incidents],
      row[:unresolved_incidents],
      row[:unresolved_rate_percent],
      avg
    ].join(",")
  end
end

if ARGV.length != 1
  warn "Usage: ruby service_report.rb <incidents.jsonl>"
  exit 1
end

input_path = ARGV[0]
unless File.exist?(input_path)
  warn "Input file not found: #{input_path}"
  exit 1
end

rows = build_service_report(read_incidents(input_path))
print_report(rows)
