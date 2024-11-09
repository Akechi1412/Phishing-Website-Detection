import ProTypes from 'prop-types';

function ProgressCircle({ percentage, size = 100 }) {
  const strokeWidth = 8;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const progress = circumference * (1 - percentage / 100);

  const getColor = (percentage) => {
    if (percentage > 75) return 'text-red-500';
    if (percentage > 50) return 'text-orange-500';
    if (percentage > 25) return 'text-yellow-500';
    return 'text-green-500';
  };

  return (
    <div className="flex justify-center items-center">
      <svg
        className="transform -rotate-90"
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
      >
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth={strokeWidth}
          className="text-gray-200"
        />

        {percentage >= 0 ? (
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke="currentColor"
            strokeWidth={strokeWidth}
            className={getColor(percentage)}
            strokeDasharray={circumference}
            strokeDashoffset={progress}
            style={{ transition: 'stroke-dashoffset 0.5s ease' }}
          />
        ) : (
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke="currentColor"
            strokeWidth={strokeWidth}
            strokeDasharray="4 8"
            className="text-gray-400"
          />
        )}
      </svg>
      <span className="absolute text-lg font-semibold text-primary">
        {percentage >= 0 ? `${percentage}%` : 'N/A'}
      </span>
    </div>
  );
}

ProgressCircle.propTypes = {
  percentage: ProTypes.number.isRequired,
  size: ProTypes.number,
};

export default ProgressCircle;
