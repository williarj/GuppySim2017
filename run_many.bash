for i in `seq 1 50`;
do
    #python guppy.py  > ../output/default_$i.txt
    #python guppy.py  -c 0.7 > ../output/highC_$i.txt
    #python guppy.py --no_c -s 0 > ../output/no_s_$i.txt
    #python guppy.py --no_c -s 0.5  > ../output/highS_$i.txt
    #python guppy.py --no_c -s 0.25  > ../output/medS_$i.txt
    python guppy.py --no_c -m 2  > ../output/no_c_12m_$i.txt
    #python guppy.py --no_c -N 12 -m 0.5  > ../output/no_c_12f_$i.txt
    #python guppy.py --no_c -m 2 --no_r  > ../output/no_c_r_12m_$i.txt
    #python guppy.py --no_r  > ../output/no_r_$i.txt
    #python guppy.py --no_c  > ../output/no_c_$i.txt
    #python guppy.py --no_p > ../output/no_p_$i.txt
    
    #python guppy.py --no_p --no_r > ../output/no_p_r_$i.txt
    #python guppy.py --no_p --no_c > ../output/no_p_c_$i.txt
done

wait $!

python cleanup.py ../output/default_*.txt > ../data/default_avg.txt
python cleanup.py ../output/no_r_*.txt > ../data/no_r_avg.txt
python cleanup.py ../output/no_c_[0-9].txt ../output/no_c_[0-9][0-9].txt> ../data/no_c_avg.txt

python cleanup.py ../output/no_p_r_*.txt > ../data/no_p_r_avg.txt
python cleanup.py ../output/no_p_c_*.txt > ../data/no_p_c_avg.txt

#this one is wierd so it will not pool the other no_p runs
python cleanup.py ../output/no_p_[0-9].txt ../output/no_p_[0-9][0-9].txt > ../data/no_p_avg.txt

#testers
python cleanup.py ../output/highC_*.txt > ../data/highC_avg.txt
python cleanup.py ../output/medS_*.txt > ../data/medS_avg.txt
python cleanup.py ../output/no_s_*.txt > ../data/no_s_avg.txt
python cleanup.py ../output/highS_*.txt > ../data/highS_avg.txt
python cleanup.py ../output/no_c_12f_*.txt > ../data/no_c_12f_avg.txt
python cleanup.py ../output/no_c_12m_*.txt > ../data/no_c_12m_avg.txt
python cleanup.py ../output/no_c_r_12m_*.txt > ../data/no_c_r_12m_avg.txt



#gets the OBS values
python cleanup.py ../output/default_*.txt -p "Observed values" > ../data/default_obs_avg.txt
python cleanup.py ../output/no_r_*.txt -p "Observed values" > ../data/no_r_obs_avg.txt
python cleanup.py ../output/no_c_[0-9].txt ../output/no_c_[0-9][0-9].txt -p "Observed values" > ../data/no_c_obs_avg.txt

python cleanup.py ../output/no_p_r_*.txt -p "Observed values" > ../data/no_p_r_obs_avg.txt
python cleanup.py ../output/no_p_c_*.txt -p "Observed values" > ../data/no_p_c_obs_avg.txt

#this one is wierd so it will not pool the other no_p runs
python cleanup.py ../output/no_p_[0-9].txt ../output/no_p_[0-9][0-9].txt -p "Observed values" > ../data/no_p_obs_avg.txt

#testers
python cleanup.py ../output/highC_*.txt -p "Observed values" > ../data/highC_obs_avg.txt
python cleanup.py ../output/medS_*.txt -p "Observed values" > ../data/medS_obs_avg.txt
python cleanup.py ../output/no_s_*.txt -p "Observed values" > ../data/no_s_obs_avg.txt
python cleanup.py ../output/highS_*.txt -p "Observed values" > ../data/highS_obs_avg.txt
python cleanup.py ../output/no_c_12f_*.txt -p "Observed values" > ../data/no_c_12f_obs_avg.txt
python cleanup.py ../output/no_c_12m_*.txt -p "Observed values" > ../data/no_c_12m_obs_avg.txt
python cleanup.py ../output/no_c_r_12m_*.txt > ../data/no_c_r_12m_obs_avg.txt

