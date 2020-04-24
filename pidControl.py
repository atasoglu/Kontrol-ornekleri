class pidControl:
    def __init__(self, Ref, Sampling_Time, PID = [1, 0, 0]):
        self.set_ref(Ref)
        self.set_sampling_time(Sampling_Time)
        self.set_params(PID)
        self.clear()

    def get_ref(self):
        return self.ref
    def get_sampling_time(self):
        return self.dt
    def get_params(self):
        return self.params
    def get_sys_model(self):
        return self.sys_model
    def get_K(self, str_param):
        if str_param in self.params: 
            return self.params[str_param]
    def set_ref(self, r):
        self.ref = r
    def set_sampling_time(self, t):
        self.dt = t
    def set_params(self, arr):
        self.params = {
            'p': arr[0],
            'i': arr[1],
            'd': arr[2]
        }
    def set_sys_model(self, func):
        self.sys_model = func
    def set_K(self, str_param, value):
        if str_param in self.params:
            self.params[str_param] = value
    
    def clear(self):
        self.A = 0
        self.last_err = 0
      
    def PID(self, func, step, last_err = 0, A = 0, out = [0]):
        if step < 1: return out
        e = self.ref - out[-1]
        A += self.dt * (e + last_err) / 2
        u = self.params['p'] * e + self.params['i'] * A + self.params['d'] * (e - last_err) / self.dt
        c = func(u)
        return self.PID(func, step-1, e, A, out+[c])
    
    def one_shot(self, fb_value):
        e = self.ref - fb_value
        self.A += self.dt * (e + self.last_err) / 2
        P = self.params['p'] * e
        I = self.params['i'] * self.A
        D = self.params['d'] * (e - self.last_err) / self.dt
        u = P + I + D 
        self.last_err = e
        return self.sys_model(u)

