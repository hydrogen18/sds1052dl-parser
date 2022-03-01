
def parse_header_line(accum, line):
  line = line.split(',')

  if line[0] == 'Record Length':
    record_count = int(line[1].strip())
    data_sources = []
    offset = 2
    for i, x in enumerate(line[offset:]):
      if len(x) > 0:
        data_sources.append((i + offset, x.strip(),))
    accum['record_count'] = record_count
    accum['data_sources'] = sorted(data_sources, key = lambda x : x[0])

  elif line[0] == 'Sample Interval':
    data = line[1].split(' ')
    sample_intervals = {}
    for x in data:
      source_name, value = x.split(':')
      value = float(value)
      sample_intervals[source_name] = value
    accum['sample_intervals'] = sample_intervals
  elif line[0] == 'Vertical Units':
    data = line[1].split(' ')
    vertical_units = {}
    for x in data:
      source_name, value = x.split(':')
      vertical_units[source_name] = value
    accum['vertical_units'] = vertical_units
  elif line[0] == 'Vertical Scale':
    data = line[1].split(' ')
    vertical_scale = {}
    for x in data:
      source_name, value = x.split(':')
      vertical_scale[source_name] = float(value)
    accum['vertical_scale'] = vertical_scale
  elif line[0] == 'Vertical Offset':
    data = line[1].split(' ')
    vertical_offset = {}
    for x in data:
      source_name, value = x.split(':')
      vertical_offset[source_name] = float(value)
    accum['vertical_offset'] = vertical_offset
  elif line[0] == 'Horizontal Units':
    accum['horizontal_units'] = line[1]
  elif line[0] == 'Horizontal Scale':
    accum['horizontal_scale'] = float(line[1])

def parse_file_raw(fin):
  headers = {}
  headers_done = False
  output = []
  for line in fin:
    if len(line) == 0:
      continue
    if not headers_done:
      if line[0].isalpha():
        parse_header_line(headers, line)
        continue
      else:
        headers_done = True
    output.append(parse_data_line(headers, line))

  return (headers, output)

def parse_file(fin):
  headers, raw_data = parse_file_raw(fin)
  output = []
  data_sources = [name for _, name in headers['data_sources']]
  for entry in raw_data:
    data_line = []
    for i, data_point in enumerate(entry):
      name = data_sources[i]
      if name == 'Source':
         data_line.append(data_point * headers['horizontal_scale'])
      else:
         data_line.append(data_point * headers['vertical_scale'][name])
    output.append(data_line)

  headers['parsed_data_sources'] = {name: i for i,name in enumerate(data_sources) }
  return headers, output
      

def parse_data_line(accum, line):
  line = line.split(',')
  data = []
  for (i, data_source) in accum['data_sources']:
    data.append(float(line[i]))
  return data
