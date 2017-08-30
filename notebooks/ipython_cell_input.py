class Progression:
    
    def __init__(self, start_date, length, progressions):
        self.start_date = start_date
        self.length = length
        self.sessions = []
        
        progress_dict = {
            "runeasy": self.runeasy,
            "interval": self.interval
        }
        
        start = 0
        step = len(progressions)
        
        for progression in progressions:
            self.sessions += [wk for wk in progress_dict[progression[0]](start, step, progression[1])]     
            start += 1  
        
        
    def runeasy(self, start, step, settings):
        '''
        '''

        wk = start

        dur = settings.init_dur

        while wk < self.length:
            if week_type(wk, self.length) == 'prog':
                if (wk + 1) % settings.prog_freq == 0 and dur < settings.max_dur:
                    dur += 5
                wk_dur = dur
            elif week_type(wk, self.length) == 'rest':
                wk_dur = rest_pc_or_abs(settings.rest, dur)
            else:
                wk_dur = rest_pc_or_abs(settings.race, dur)

            # Build workout
            date = self.start_date + timedelta(weeks=wk)
            w = Workout(date, 'RunEasy')
            ws = WorkoutSet(1)
            e = Exercise('Easy', wk_dur)
            ws.add_exercise(e)
            w.add_workoutset(ws)           

            yield w

            wk += step
    
    def interval(self, start, step, settings):
        '''
        '''

        wk = start

        dur = settings.init_dur

        while wk < self.length:
            if week_type(wk, self.length) == 'prog':
                if (wk + 1) % settings.prog_freq == 0 and dur < settings.max_dur:
                    dur += 5
                wk_dur = dur
            elif week_type(wk, self.length) == 'rest':
                wk_dur = rest_pc_or_abs(settings.rest, dur)
            else:
                wk_dur = rest_pc_or_abs(settings.race, dur)

            # Build workout
            date = self.start_date + timedelta(weeks=wk)
            w = Workout(date, 'Interval')
            ws = WorkoutSet(1)
            e = Exercise('Easy', wk_dur)
            ws.add_exercise(e)
            w.add_workoutset(ws)           

            yield w

            wk += step

            
class Plan:
    '''
    Represents running training plan for prescribed event and level.
    '''
    
    def __init__(self, distance, level, start_date, event_date, event_title):
        
        self.distance = distance
        self.level = level
        self.start_date = start_date
        self._event_date = event_date
        self.event_title = event_title
        

        # Populate schedule with event
        self.schedule = [Workout(self._event_date, 'Event Day')]

    @property
    def length(self):
        '''
        Length of the training plan in weeks
        '''
        return self.weeks_between_dates(self.start_date, self._event_date)

    def create(self, days):
        '''
        Creates schedule based on ability level and training days
        '''
        
        details = PLANS[self.distance][self.level]
        
        for day, detail in zip(days, details):
            session_start = determine_next_weekday(self.start_date, day)
            p = Progression(session_start, self.length, detail)
            self.schedule += p.sessions

    def __repr__(self):
        '''
        Return a more human-readable representation
        '''

        return "{0} week {1} Plan for the {2}".format(self.length,
                                                      self.level,
                                                      self.event_title)

    @property
    def event_date(self):
        '''
        Event date property, formatted as a string
        '''
        return self._event_date.strftime('%d %b %Y')

    @staticmethod
    def weeks_between_dates(start_date, end_date):
        '''
        Return the number of weeks between two dates
        '''
        return int((determine_next_weekday(end_date, 0) -
                    determine_next_weekday(start_date, 0)).days / 7)

    
from datetime import date, timedelta
start_date = date(2017, 8, 25)
event_date = start_date + timedelta(weeks=4)
p = Plan('5k', 'Beginner', start_date, event_date, 'RACE DAY')

days = [0, 2]
p.create(days)