import random


class Reader:
    def init(self, filename):
        self.filename = filename
    ##reading 
    def raw_data(self):
        raw = ""
        file = open(self.filename, mode="r", encoding="utf-8-sig")
        for string in file:
            raw = raw + string
        file.close()
        return raw
    ##adding encoded_chars to table
    def ec_data(self, raw):
        ec_data = []
        for x in raw:
            ec_data.append(self.char_encoded(x))
        return ec_data

    def char_encoded(self, char):
    ##getting ascii_char with ctrl_sum
        asci = str(ord(char))
        ctrl_sum = self._calc_control_sum(asci)
    ##counting how many marks does ascii_char have to check how many 0 to add
        if len(asci) == 1:
            asci = "00" + asci
        elif len(asci) == 2:
            asci = "0" + asci
    ##getting random ISN 10 number range (we checked that before, explained in documentation)
        rand = str(self._get_random(1000020914, 4294873279))
    ##adding encoded to ISN    
        for i, x in enumerate(asci):
            step = (i+1) * 3
            rand = "".join([rand[:step-1], x, rand[step:]])
        
        new_ctrl_sum = self._new_ctrl_sum(asci)
        rand = "".join([rand[:3], new_ctrl_sum[0], rand[4:]])
        rand = "".join([rand[:7], new_ctrl_sum[1], rand[8:]])

        return [int(rand), int(ctrl_sum)]
    ##creating new ctrlsum
    def new_ctrl_sum(self, asci):
        ctrl_sum = 0
        for x in asci:
            ctrl_sum = ctrl_sum + int(x)

        ctrl_sum = str(ctrl_sum)
        if len(ctrl_sum) == 1:
            ctrl_sum = "0" + ctrl_sum
        return ctrl_sum
    ##calculating control_sum
    def calc_control_sum(self, asci):
        ctrl_sum = 0
        for x in asci:
            ctrl_sum = ctrl_sum + int(x)

        ctrl_sum = str(ctrl_sum)
        if len(ctrl_sum) == 1:
            ctrl_sum = "0" + ctrl_sum
    ##3268-63998 is range of ports
        rand = str(self._get_random(32768, 63998))
        for i, x in enumerate(ctrl_sum):
            step = i * 2 + 3
            rand = "".join([rand[:step-1], x, rand[step:]])

        return rand
        
    def get_random(self, from_n, to_n):
        randgen = random.SystemRandom()
        return randgen.randrange(from_n, to_n)
