import csv

poses = [
    ['name','description','benefits','difficulty','category','search_tags'],
    ['Mountain Pose','Stand tall with feet together','Improves posture,Strengthens thighs,Increases awareness','Beginner','standing','posture,beginner,standing,foundation'],
    ['Warrior I','Step back and bend front knee','Strengthens legs,Opens hips,Improves focus','Beginner','standing','legs,hips,balance,strength,beginner'],
    ['Warrior II','Wide stance with arms extended','Strengthens legs,Stretches hips,Builds stamina','Beginner','standing','legs,arms,strength,stamina,beginner'],
    ['Tree Pose','Balance on one leg with foot on thigh','Improves balance,Strengthens legs,Builds focus','Beginner','balance','balance,focus,legs,beginner,stability'],
    ['Child Pose','Kneel and stretch arms forward','Relieves back pain,Calms mind,Stretches hips','Beginner','restorative','back pain,rest,relaxation,beginner,stretching'],
    ['Downward Dog','Inverted V shape with hands and feet','Stretches hamstrings,Strengthens arms,Energizes body','Beginner','standing','hamstrings,arms,energy,beginner,stretching'],
    ['Triangle Pose','Wide stance with side stretch','Stretches legs,Opens chest,Improves digestion','Beginner','standing','legs,chest,digestion,beginner,stretching'],
    ['Cobra Pose','Lie face down and lift chest','Strengthens spine,Opens chest,Relieves stress','Beginner','backbend','spine,chest,stress,beginner,backbend'],
    ['Seated Forward Bend','Sit and reach for toes','Stretches hamstrings,Calms mind,Relieves anxiety','Beginner','seated','hamstrings,anxiety,calm,beginner,seated'],
    ['Bridge Pose','Lie on back and lift hips','Strengthens back,Opens chest,Reduces anxiety','Beginner','backbend','back,chest,anxiety,beginner,backbend'],
    ['Cat Cow Pose','Arch and round your back on all fours','Improves spine flexibility,Relieves back pain,Warms up body','Beginner','core','back pain,spine,flexibility,beginner,warm up'],
    ['Plank Pose','Hold push up position','Strengthens core,Tones arms,Builds endurance','Beginner','core','core,arms,strength,beginner,endurance'],
    ['Camel Pose','Kneel and reach back for heels','Opens chest,Strengthens back,Improves posture','Intermediate','backbend','chest,back,posture,intermediate,backbend'],
    ['Pigeon Pose','Deep hip opener on the floor','Opens hips,Releases tension,Stretches thighs','Intermediate','hip opening','hips,tension,thighs,intermediate,hip opening'],
    ['Boat Pose','Balance on sit bones with legs raised','Strengthens core,Improves balance,Tones abs','Intermediate','core','core,balance,abs,intermediate,strength'],
    ['Crow Pose','Balance on hands with knees on arms','Strengthens arms,Builds focus,Tones core','Intermediate','balance','arms,focus,core,intermediate,balance'],
    ['Headstand','Balance upside down on head','Improves circulation,Builds strength,Calms mind','Advanced','inversion','circulation,strength,calm,advanced,inversion'],
    ['Shoulder Stand','Balance on shoulders with legs up','Improves thyroid,Calms nervous system,Strengthens core','Advanced','inversion','thyroid,calm,core,advanced,inversion'],
    ['Lotus Pose','Sit cross legged with feet on thighs','Improves posture,Calms mind,Opens hips','Intermediate','seated','posture,calm,hips,intermediate,meditation'],
    ['Half Moon Pose','Balance on one leg with side stretch','Improves balance,Strengthens legs,Opens hips','Intermediate','balance','balance,legs,hips,intermediate,stretching'],
]

with open('database/yoga_poses.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(poses)

print(f'✅ CSV created with {len(poses)-1} poses!')