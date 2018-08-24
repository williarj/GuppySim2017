out="~/Desktop/simulation_results" #leave this as an empty string to not save to file ~/Desktop/simulation_results.eps
input = "~/Desktop/simulation_data.csv"

if (out !=""){
  setEPS()
  postscript(paste(out, "1.eps", sep=""))
}

#************IMPORTANT***************
#for the three variables below (plot_X):
#set to FALSE to exclude the line from the plot
#set to TRUE to include it
plot_bro = TRUE
plot_no = TRUE
plot_nonkin = TRUE

#These two variables will turn on the 
#observed and expected data points/lines
observed = TRUE
expected = FALSE

#The order below here matters, dont mess with it
colors1 = c()
colors2 = c()
if (plot_no == TRUE){
  types = append(types, "No rival")
  colors1 = append(colors1, "black")
  colors2 = append(colors2, "black")
}else{
  colors1 = append(colors1, "white")
  colors2 = append(colors2, rgb(245/255,245/255,245/255))
}
if (plot_nonkin == TRUE){
  types = append(types, "Non-kin rival")
  colors1 = append(colors1, "black")
  colors2 = append(colors2, "black")
}else{
  colors1 = append(colors1, "white")
  colors2 = append(colors2, rgb(245/255,245/255,245/255))
}
if (plot_bro == TRUE){
  types = c("Brother rival")
  colors1 = append(colors1, "black")
  colors2 = append(colors2, "black")
}  else{
  colors1 = append(colors1, "white")
  colors2 = append(colors2, rgb(245/255,245/255,245/255))
}
####END WEIRD SINGLE LINE PLOT STUFF


Multiv <- read.csv(input, header=TRUE)
Multiv$size = factor(Multiv$size, levels=c("Small", "Medium", "Large"))
Multiv$context = factor(Multiv$context, levels=c("No rival", "Non-kin rival", "Brother rival"))
Multiv = with(Multiv, Multiv[order(trial, size, context),])
#Multiv = subset(Multiv, subset=(Multiv$Cont %in% types))

library(plotrix)


#agdata = aggregate(Multiv, by=list(Multiv$Cont, Multiv$F), FUN=mean)
#agerror = aggregate(Multiv, by=list(Multiv$Cont, Multiv$F), FUN=std.error)

par(las = 1) #can modify text size using this line, but probably easier to do in ppt

plotTrial <- function(subdata, name, legend_pos='topleft', legend_pres=TRUE, ylim=c(0,1), xaxis=FALSE, obs=FALSE){
  #subdata=with(subdata, subdata[order(context, size),])
  gap = 0.2
  C=1.4
  xs=c(1,1.5,2,3,3.5,4,5,5.5,6)
  x=plotCI(xs, subdata$avg, col="white",
           uiw=subdata$se, pch=c(1,0,2),
           #xlim=c(xs[1]-0.4, xs[9]+0.4),
           #yaxt='n',
           ylim=ylim,
           cex=C, xaxt='n', bty='n',
           xlab="", ylab='Male mating effort')
  
  offset = (xs[2]-xs[5])/2
  rect(xs[5]+offset+gap/2, -.1, xs[8]+offset+gap/2, 1.1, border=NA, col=rgb(245/255,245/255,245/255) )
  #axis(2, at=seq(0, .3, .06))
  
  plotCI(xs, subdata$avg, col=colors2, xlim=c(xs[1]-0.4, xs[9]+0.4), add=TRUE, yaxt='n'
         , uiw=subdata$se, pch=c(1,0,2), 
         ylim=ylim, 
         cex=C, xaxt='n', bty='n', ylab='Male mating effort')
  if (plot_no==TRUE) lines(xs[seq(1,9,3)], subdata[subdata$context=="No rival",]$avg)
  if (plot_nonkin==TRUE) lines(xs[seq(2,9,3)], subdata[subdata$context=="Non-kin rival",]$avg)
  if (plot_bro==TRUE) lines(xs[seq(3,9,3)], subdata[subdata$context=="Brother rival",]$avg)
 
  if (obs != FALSE){
    c='red'
    plotCI(xs, obs$avg, col=c, xlim=c(xs[1]-0.4, xs[9]+0.4), add=TRUE, yaxt='n'
           , uiw=obs$se, pch=c(1,0,2), 
           ylim=ylim, 
           cex=C)
    if (plot_no==TRUE) lines(xs[seq(1,9,3)], obs[obs$context=="No rival",]$avg, col=c)
    if (plot_nonkin==TRUE) lines(xs[seq(2,9,3)], obs[obs$context=="Non-kin rival",]$avg, col=c)
    if (plot_bro==TRUE) lines(xs[seq(3,9,3)], obs[obs$context=="Brother rival",]$avg, col=c)
    
  }
  
  axis(1, at=c(0.5, xs[c(5,8)]+offset+gap/2, 6.5), labels=c("", "", "", ""))
  if (xaxis == TRUE){
    axis(1, at=c(xs[c(2,5,8)]+gap/2), labels=c("Small", "Medium", "Large"), lwd=0)
    title(name, xlab="Female size")
  }else{
    title(name)
  }
  if (legend_pres == TRUE){
    legend(legend_pos, c("No rival", "Non-kin rival", "Brother rival"), y.intersp=0.7, pch=c(1,0,2), bty='n', cex=1)
  }
}


par(mfrow=c(3,2),
    oma = c(5,4,0,0) + 0.1,
    mar = c(1.2,4,1.5,0) + 0.1)

lim = c(0.0, 0.3)

plotTrial(Multiv[Multiv$trial=="default",], "(A) All Parameters", ylim=lim, obs = Multiv[Multiv$trial=="default_obs",])
#plotTrial(Multiv[Multiv$trial=="highC",], "C=7", legend_pres=FALSE, ylim=lim, obs = Multiv[Multiv$trial=="highC_obs",])
plotTrial(Multiv[Multiv$trial=="no_c",], "(B) C=0 ", legend_pres=FALSE, ylim=lim, obs = Multiv[Multiv$trial=="no_c_obs",])
#plotTrial(Multiv[Multiv$trial=="no_c_12f",], "C=012f", legend_pres=FALSE, ylim=lim, obs = Multiv[Multiv$trial=="no_c_12f_obs",])
#plotTrial(Multiv[Multiv$trial=="no_c_12m",], "C=0 12m", legend_pres=FALSE, ylim=lim, obs = Multiv[Multiv$trial=="no_c_12m_obs",])
#plotTrial(Multiv[Multiv$trial=="no_c_r_12m",], "Cr 12m", legend_pres=FALSE, ylim=lim, obs = Multiv[Multiv$trial=="no_c_r_12m_obs",])
#par(mar = c(4,4,1,0))
#plotTrial(Multiv[Multiv$trial=="highS",], "C= 0 STOP=0.5", c(1, 2050), legend_pres=FALSE, ylim=lim, xaxis=TRUE, obs = Multiv[Multiv$trial=="highS_obs",])
plotTrial(Multiv[Multiv$trial=="no_p",], "(C) P=1", c(1, 1850), legend_pres=FALSE, ylim=lim, xaxis=FALSE, obs = Multiv[Multiv$trial=="no_p_obs",])
plotTrial(Multiv[Multiv$trial=="no_p_c",], "(D) C=0; P=1", c(1, 1850), legend_pres=FALSE, ylim=lim, xaxis=TRUE, obs = Multiv[Multiv$trial=="no_p_c_obs",])
plotTrial(Multiv[Multiv$trial=="no_r",], "(E) r=0", c(1, 1850), legend_pres=FALSE, ylim=lim, xaxis=TRUE, obs = Multiv[Multiv$trial=="no_r_obs",])

if (out !=""){
  dev.off()
  postscript(paste(out, "2.eps", sep=""))
}

par(mfrow=c(1,2))

plotTrial(Multiv[Multiv$trial=="medS",], "(A) C=0 STOP=0.25", c(1, 2250), legend_pres=TRUE, ylim=lim, xaxis=TRUE, obs = Multiv[Multiv$trial=="medS_obs",])
plotTrial(Multiv[Multiv$trial=="no_s",], "(B) C=0 STOP=0", c(1, 2250), legend_pres=FALSE, ylim=lim, xaxis=TRUE, obs = Multiv[Multiv$trial=="no_s_obs",])


if(out!=""){
  dev.off()
}
