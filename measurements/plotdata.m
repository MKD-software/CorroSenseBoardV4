
plot(TRACE01MAGPHASE.KeysightTechnologi/1000, TRACE01MAGPHASE.A0302)

%%

plot(sweep200.FrequencyHz,movmean(sweep200.Phase,1))
hold on
%%

plot(sweep200.FrequencyHz,movmean(sweep200.Magnitude,100))

%%

plot(sweep1.FrequencyHz,movmean(sweep1.Phase,1))
%%

plot(sweep1.FrequencyHz,movmean(sweep1.Magnitude,1))

%%

plot(TIA0.FrequencyHz,movmean(TIA0.Phase,1))
hold on
plot(TIA50.FrequencyHz,movmean(TIA50.Phase,1))
plot(TIA100.FrequencyHz,movmean(TIA100.Phase,1))
plot(TIA150.FrequencyHz,movmean(TIA150.Phase,1))

%%

plot(sweep9.FrequencyHz,movmean(sweep10.Phase,1))

%%

phaseraw = sweep10.Phase;

phasedeg = (2*pi*(phaseraw/2800));

plot(sweep9.FrequencyHz,phaseraw)
%%
plot(TRACE01MAGPHASE.KeysightTechnologi/1000, TRACE01MAGPHASE.A0302)

%%
phasedeg = (2 * pi * (phaseraw / 2800));

plot(phasedeg)



