program statistics
  use types, only: dp
  use math, only: mean,avevar
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  implicit none
  integer :: n,i,io,is,count
  real(dp) :: offset,step,a,v,m,wmean,expected_mean,expected_var,expected_weighted,e,maximum
  real(dp), allocatable :: x(:),w(:)
  maximum=0;count=0
  do n=2,20
    allocate(x(n),w(n))
    w=[(real(i,dp),i=1,n)]
    do io=0,1
      offset=10.0_dp*io
      do is=0,2
        step=0.25_dp*4.0_dp**is
        x=offset+step*w
        expected_mean=offset+step*real(n+1,dp)/2
        expected_var=step**2*real(n*(n+1),dp)/12
        expected_weighted=offset+step*real(2*n+1,dp)/3
        m=mean(x);wmean=mean(x,w)
        call avevar(x,a,v)
        if(.not.all(ieee_is_finite([m,wmean,a,v])))error stop 'Nonfinite statistics'
        e=max(abs(m-expected_mean)/max(1.0_dp,abs(expected_mean)), &
          abs(a-expected_mean)/max(1.0_dp,abs(expected_mean)), &
          abs(wmean-expected_weighted)/max(1.0_dp,abs(expected_weighted)), &
          abs(v-expected_var)/expected_var)
        if(e>2e-12_dp)error stop 'Closed-form statistics mismatch'
        maximum=max(maximum,e);count=count+1
      end do
    end do
    deallocate(x,w)
  end do
  print '(a,i0)', 'Closed-form statistics cases: ',count
  print '(a,es14.6)', 'Maximum normalized statistic error: ',maximum
  print '(a)', 'PASS statistics'
end program
