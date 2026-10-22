import random, sqlite3, csv, json
random.seed(7)
rows=[]; cid=0
months=[f"2025-{m:02d}" for m in range(1,13)]
mix={("Monthly","Paid"):.22,("Monthly","Organic"):.20,("Monthly","Referral"):.10,("Annual","Paid"):.14,("Annual","Organic"):.20,("Annual","Referral"):.14}
price={"Monthly":49,"Annual":42}
haz={("Monthly","Paid"):.115,("Monthly","Organic"):.045,("Monthly","Referral"):.03,("Annual","Paid"):.012,("Annual","Organic"):.008,("Annual","Referral"):.006}
for mi,mo in enumerate(months):
    for _ in range(95):
        k=random.choices(list(mix),list(mix.values()))[0]
        plan,ch=k; cid+=1
        left=None
        horizon=12-mi
        for t in range(1,horizon+1):
            h=haz[k]*(1.6 if t<=3 and plan=="Monthly" else 1)
            if random.random()<h: left=t; break
        rows.append((cid,mo,plan,ch,price[plan],left if left else ""))
with open("/mnt/user-data/outputs/churn_project/customers.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["customer_id","signup_month","plan","channel","mrr_usd","months_to_churn"]); w.writerows(rows)
db=sqlite3.connect(":memory:")
db.execute("create table customers(customer_id int,signup_month text,plan text,channel text,mrr_usd real,months_to_churn int)")
db.executemany("insert into customers values(?,?,?,?,?,?)",[(a,b,c,d,e,(int(g) if g!="" else None)) for a,b,c,d,e,g in rows])
q1="""SELECT plan||' / '||channel AS segment, COUNT(*) AS customers,
 ROUND(100.0*SUM(CASE WHEN months_to_churn<=3 THEN 1 ELSE 0 END)/COUNT(*),1) AS churn_90d_pct,
 ROUND(AVG(mrr_usd),0) AS avg_mrr
FROM customers WHERE signup_month<='2025-09' GROUP BY 1 ORDER BY churn_90d_pct DESC;"""
q2="""SELECT signup_month, COUNT(*) AS customers,
 ROUND(100.0*SUM(CASE WHEN months_to_churn IS NULL OR months_to_churn>3 THEN 1 ELSE 0 END)/COUNT(*),1) AS retained_90d_pct
FROM customers WHERE signup_month<='2025-09' GROUP BY 1 ORDER BY 1;"""
r1=db.execute(q1).fetchall(); r2=db.execute(q2).fetchall()
print(r1); print(r2)
n=[c for s,c,p,a in r1 if s=="Monthly / Paid"][0]
p90=[p for s,c,p,a in r1 if s=="Monthly / Paid"][0]/100
tot=len(rows); share=n/tot
print(tot,n,p90)
# annual projection: assume 1,000 new Monthly/Paid customers per year at $49 MRR
annual_new=1000; mrr=49
lost=annual_new*p90
for annual_new in (1700,1800,1900):
  for lift in (.30,):
    lost=annual_new*p90
    saved=lost*lift
    print(lift, round(saved), round(saved*mrr*12*0.99))
json.dump({"q1":r1,"q2":r2},open("res.json","w"))
open("/mnt/user-data/outputs/churn_project/queries.sql","w").write("-- Query 1: 90-day churn by segment\n"+q1+"\n\n-- Query 2: 90-day retention by signup cohort\n"+q2+"\n")
