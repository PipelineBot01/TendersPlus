NUM_TOPICS = 22  # total topics that are set in lda model
NUM_SHOW_TERM = 20  # the number of words in the topic that want to be showed
PROJECT_STOP_WORDS = ['-', '/', '21st', 'able', 'academic', 'access', 'accessible', 'accordance', 'achievement',
                      'acquisition', 'action', 'active', 'activity', 'actual', 'acute', 'ad', 'additional',
                      'administration', 'advanced', 'advantage', 'advice', 'agency', 'agreement', 'aim', 'analyse',
                      'analysis', 'annual', 'applicant', 'approach', 'appropriate', 'apr', 'april', 'area',
                      'assistance', 'assurance', 'ation', 'aug', 'august', 'aus', 'australasian', 'australia',
                      'australian', 'available', 'award', 'awareness', 'base', 'basic', 'basis', 'best', 'bid',
                      'bidding', 'business', 'calendar', 'capability', 'capable', 'capacity', 'capital', 'capture',
                      'career', 'case', 'category', 'centre', 'challenge', 'claim', 'close', 'collaboration',
                      'collection', 'combination', 'command', 'commonwealth', 'community', 'competitive', 'complex',
                      'component', 'comprehensive', 'concept', 'connection', 'consortium', 'content', 'continuation',
                      'continuity', 'contribution', 'cooperation', 'cooperative', 'core', 'creative', 'creek', 'cross',
                      'current', 'da', 'date', 'day', 'dec', 'december', 'decision', 'deed', 'delivery', 'demand',
                      'department', 'depment', 'description', 'detailed', 'development', 'disadvantaged', 'draft',
                      'early', 'east', 'effect', 'effective', 'effectiveness', 'efficiency', 'efficient', 'effort',
                      'element', 'eligible', 'employment', 'enable', 'end', 'engagement', 'enhance', 'entry', 'er',
                      'essential', 'event', 'ex', 'example', 'excellence', 'experience', 'experienced', 'expert',
                      'expertise', 'extension', 'external', 'feb', 'february', 'field', 'first', 'fit', 'focus',
                      'focused', 'following', 'forgotten', 'form', 'friday', 'function', 'fund', 'funding', 'future',
                      'general', 'goal', 'good', 'government', 'grant', 'great', 'group', 'half', 'headquarters',
                      'high', 'hub', 'ian', 'idea', 'implementation', 'importance', 'important', 'improved',
                      'inclusion', 'inclusive', 'increase', 'independent', 'index', 'individual', 'industry',
                      'information', 'ing', 'initial', 'institute', 'institution', 'intended', 'interested',
                      'invitation', 'invite', 'involvement', 'issue', 'ist', 'jan', 'january', 'job', 'joint', 'jul',
                      'july', 'jun', 'june', 'key', 'knowledge', 'left', 'level', 'line', 'linkage', 'list', 'location',
                      'long', 'loss', 'low', 'ly', 'major', 'making', 'mar', 'march', 'maximum', 'may', 'medium',
                      'method', 'methodology', 'mid', 'minimum', 'mis', 'mission', 'monday', 'monitoring', 'month',
                      'mt', 'mutual', 'national', 'necessary', 'need', 'new', 'non', 'north', 'notice', 'nov',
                      'november', 'oat', 'objective', 'oct', 'october', 'offer', 'office', 'officer', 'ongoing', 'open',
                      'opportunity', 'option', 'order', 'organisation', 'ot', 'outcome', 'outline', 'outstanding',
                      'pack', 'package', 'participant', 'participation', 'past', 'people', 'period', 'personnel',
                      'phase', 'phd', 'place', 'platform', 'position', 'positive', 'practice', 'practitioner', 'pre',
                      'primary', 'prime', 'priority', 'process', 'processing', 'professional', 'program', 'programme',
                      'project', 'promulgation', 'proof', 'proposal', 'provide', 'provision', 'pty', 'purpose',
                      'qualified', 'quality', 'range', 'rare', 'rate', 'ready', 'recipient', 'recommendation', 'refer',
                      'register', 'related', 'relevant', 'replacement', 'request', 'requirement', 'research',
                      'resource', 'responsibility', 'responsible', 'result', 'review', 'right', 'role', 'round', 'rs',
                      'saturday', 'scale', 'scholarship', 'scientific', 'scope', 'second', 'section', 'sector',
                      'senior', 'sep', 'september', 'series', 'service', 'set', 'setting', 'short', 'significant',
                      'similar', 'site', 'skill', 'small', 'smart', 'south', 'special', 'specialised', 'specialist',
                      'specific', 'specified', 'st', 'stage', 'standing', 'state', 'statement', 'strategic', 'strategy',
                      'stream', 'strong', 'sub', 'subject', 'successful', 'suitable', 'sunday', 'support', 't1',
                      'target', 'targeted', 'task', 'team', 'tender', 'tenderer', 'tenderers', 'term', 'third',
                      'thursday', 'tic', 'title', 'topic', 'total', 'training', 'tri', 'tuesday', 'ty', 'type',
                      'understanding', 'undertaking', 'unit', 'ups', 'use', 'value', 'veteran', 'way', 'wednesday',
                      'week', 'west', 'whole', 'wide', 'wish', 'work', 'world', 'www', 'year', 'young', 'zone', '???',
                      '???']

# print(sorted(set(PROJECT_STOP_WORDS)))
