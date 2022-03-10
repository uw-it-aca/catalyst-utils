import dayjs from 'dayjs';

function formatDate(dateString) {
  const date = dayjs(dateString);
  return date.format('MMMM D, YYYY');
}

export { formatDate };
