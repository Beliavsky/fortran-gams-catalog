program covariance_eigen
  use types, only: dp
  use math, only: eigencov
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  implicit none
  integer :: n,i,j,k,family,iscale,rank,cases
  real(dp) :: scale,norma,residual,orthogonality,trace_error,maxres,maxorth,maxtrace
  real(dp), allocatable :: a(:,:),p(:,:),u(:,:),d(:),gram(:,:),v(:)
  maxres=0;maxorth=0;maxtrace=0;cases=0
  do n=1,8
    allocate(a(n,n),p(n,n),u(n,n),d(n),gram(n,n),v(n))
    do family=1,4
      a=0
      select case(family)
      case(1)
        do i=1,n
          a(i,i)=real(i,dp)
        end do
      case(2)
        v=[(real(i,dp)/n,i=1,n)]
        do i=1,n
          a(:,i)=v*v(i)
        end do
      case(3)
        do i=1,n
          do j=1,n
            a(i,j)=0.5_dp**abs(i-j)
          end do
        end do
      case(4)
        do i=1,n
          do j=1,n
            gram(i,j)=sin(real(i+2*j,dp))
          end do
        end do
        a=matmul(transpose(gram),gram)
        do i=1,n
          a(i,i)=a(i,i)+0.25_dp
        end do
      end select
      do iscale=-1,1
        scale=10.0_dp**(8*iscale);p=scale*a
        call eigencov(n,p,u,d,rank,.false.)
        if(.not.all(ieee_is_finite(u)).or..not.all(ieee_is_finite(d)))error stop 'Nonfinite eigensystem'
        if(any(p/=scale*a))error stop 'Input covariance changed'
        if(any(d<0).or.rank/=count(d/=0))error stop 'Rank/nonnegative convention mismatch'
        if(any(d(1:n-1)<d(2:n)))error stop 'Eigenvalues not descending'
        norma=maxval(sum(abs(scale*a),dim=2))
        residual=0
        do k=1,n
          residual=max(residual,maxval(abs(matmul(scale*a,u(:,k))-d(k)*u(:,k)))/norma)
        end do
        gram=matmul(transpose(u),u)
        do i=1,n
          gram(i,i)=gram(i,i)-1
        end do
        orthogonality=maxval(abs(gram))
        trace_error=abs(sum(d)-sum([(scale*a(i,i),i=1,n)]))/norma
        if(max(residual,orthogonality,trace_error)>2e-11_dp)error stop 'Eigensystem invariant failed'
        if(family==1)then
          if(maxval(abs(d-[(scale*real(n-i+1,dp),i=1,n)]))/norma>2e-11_dp)error stop 'Diagonal spectrum mismatch'
        end if
        maxres=max(maxres,residual);maxorth=max(maxorth,orthogonality);maxtrace=max(maxtrace,trace_error)
        cases=cases+1
      end do
    end do
    deallocate(a,p,u,d,gram,v)
  end do
  print '(a,i0)', 'Positive-semidefinite eigensystem cases: ',cases
  print '(a,es14.6)', 'Maximum normalized eigenpair residual: ',maxres
  print '(a,es14.6)', 'Maximum orthogonality error: ',maxorth
  print '(a,es14.6)', 'Maximum normalized trace error: ',maxtrace
  print '(a)', 'PASS covariance_eigen'
end program
