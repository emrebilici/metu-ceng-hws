
setting=[0, 1, 10, 35];

no = load('no');
one = load('3-1');
two = load('3-2');
three = load('3-3');

mean_no = mean(no) / 2;
mean_one = mean(one) / 2;
mean_two = mean(two) / 2;
mean_three = mean(three) / 2;

values = [mean_no, mean_one, mean_two, mean_three];

% calculate error margin
% https://www.mathsisfun.com/data/confidence-interval.html

err_no = 1.96 * std(no) / sqrt(5);
err_one = 1.96 * std(one) / sqrt(5);
err_two = 1.96 * std(two) / sqrt(5);
err_three = 1.96 * std(three) / sqrt(5);

errors = [err_no, err_one, err_two, err_three];

figure1 = figure;
errorbar(setting, values, errors);
xlabel('Reordering Percentage (%)');
ylabel('File Transfer Time (s)');
title('File Transfer Time vs Reordering Percentage');
savefig(figure1, 'plot3.fig')
pause;

