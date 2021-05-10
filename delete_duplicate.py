i = being_fixed
while(i < len(self.inferences)-1 and self.inferences[self.being_fixed][KB.Color] == self.inferences[i+1][KB.Color]):
        if self.inferences[self.being_fixed][KB.Positions][0] in self.inferences[i+1][KB.Positions]:
            self.inferences[i+1][KB.Positions].remove(
                self.inferences[self.being_fixed][KB.Positions][0])
            if(len(self.inferences[i+1][KB.Positions]) == 1):
                self.advance_fix()
        i += 1
